"""Tests du fallback en direct (HubSpot refuse une fiche → le skill se répare → nouvel essai).

Sans réseau : fausses IA, faux HubSpot, skill copié dans un dossier temporaire.
  python -m unittest pipeline.hubspot_skill.test_heal -v
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pipeline.hubspot import send
from pipeline.hubspot_skill import heal, skill as sk
from pipeline.hubspot_skill.test_skill import HUBSPOT_PROPS, fake_chat

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = json.loads((ROOT / "data" / "contacts.sample.json").read_text(encoding="utf-8"))


class HubSpotError(Exception):
    def __init__(self, status, body):
        super().__init__(f"HubSpot HTTP {status} : {body}")
        self.status = status


class FakeHubSpot:
    """Refuse toute fiche qui utilise une propriété inconnue ou un e-mail en .example."""
    def __init__(self, known=None):
        self.known = set(known or [p["name"] for p in HUBSPOT_PROPS])
        self.calls = 0

    def __call__(self, props_list):
        self.calls += 1
        for props in props_list:
            unknown = [k for k in props if k not in self.known]
            if unknown:
                raise HubSpotError(400, f"Property \"{unknown[0]}\" does not exist")
            if str(props.get("email", "")).endswith(".example"):
                raise HubSpotError(400, f"Property values were not valid: email {props['email']}")
        return {p["bascule_legacy_id"]: f"hs-{p['bascule_legacy_id']}" for p in props_list}


class HealTest(unittest.TestCase):
    def setUp(self):
        heal.reset()
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copy(sk.SKILL_PATH, self.tmp / "skill.json")
        self.patches = [mock.patch.object(sk, "SKILL_PATH", self.tmp / "skill.json"),
                        mock.patch.object(sk, "SKILL_MD_PATH", self.tmp / "SKILL.md")]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp)
        heal.reset()

    def break_skill(self, **mapping):
        s = sk.load()
        s["mapping"].update(mapping)
        sk.save(s)

    def run_one(self, contact, hs, chat):
        with mock.patch.object(heal, "attempt", wraps=lambda e, p, r: heal_attempt(e, p, r, chat)):
            return send.migrate_one(contact, "run-heal", [], upsert=hs, write_log=lambda r: None)


def heal_attempt(error, payload, run_id, chat):
    return ORIGINAL_ATTEMPT(error, payload, run_id, chat=chat, props=HUBSPOT_PROPS)


ORIGINAL_ATTEMPT = heal.attempt

FIX_JOBTITLE = {"summary": "La propriété « jobtitle_ancien » n'existe pas : la fonction va dans « jobtitle »",
                "mapping": {"job_title": "jobtitle"}, "add_refused_email_tlds": [], "known_error":
                {"message": "Property does not exist", "cause": "propriété renommée", "action": "utiliser jobtitle"},
                "news": [], "alerts": []}
APPROVE = {"approve": True, "reasons": ["jobtitle existe dans HubSpot"]}


class TestFallback(HealTest):
    def test_propriete_renommee_reparee_puis_envoyee(self):
        self.break_skill(job_title="jobtitle_ancien")         # panne : le skill pointe vers une propriété disparue
        hs, chat = FakeHubSpot(), fake_chat(FIX_JOBTITLE, APPROVE)
        row = self.run_one(SAMPLE[0], hs, chat)
        self.assertEqual(row["status"], "success")
        self.assertEqual(row["hubspot_id"], "hs-C-0001")
        self.assertIsNone(row["error"])
        self.assertEqual(row["self_heal"]["result"], "envoyée après correction")
        self.assertIn("does not exist", row["self_heal"]["error"])
        self.assertEqual(sk.load()["mapping"]["job_title"], "jobtitle")   # skill réparé et enregistré
        self.assertEqual(hs.calls, 2)                                      # 1 échec + 1 nouvel essai

    def test_meme_erreur_fiche_suivante_sans_rappeler_les_ia(self):
        self.break_skill(job_title="jobtitle_ancien")
        hs, chat = FakeHubSpot(), fake_chat(FIX_JOBTITLE, APPROVE)
        self.run_one(SAMPLE[0], hs, chat)
        calls_after_first = list(chat.calls)
        # La fiche suivante utilise directement le skill réparé : aucun échec, aucune IA.
        row = self.run_one(SAMPLE[1], hs, chat)
        self.assertEqual(row["status"], "success")
        self.assertNotIn("self_heal", row)
        self.assertEqual(chat.calls, calls_after_first)

    def test_regle_apprise_bloque_la_fiche(self):
        s = sk.load(); s["rules"]["refused_email_tlds"] = []; sk.save(s)   # règle oubliée
        contact = {**SAMPLE[2], "email": "karim@transports-benali.example"}
        learn = {"summary": "HubSpot refuse les e-mails en .example", "mapping": {},
                 "add_refused_email_tlds": [".example"], "known_error": None, "news": [], "alerts": []}
        row = self.run_one(contact, FakeHubSpot(), fake_chat(learn, {"approve": True, "reasons": []}))
        self.assertEqual(row["self_heal"]["result"], "bloquée avant HubSpot (règle apprise)")
        self.assertEqual(row["status"], "failed")
        self.assertIn("email_refused_by_hubspot", {a["code"] for a in row["anomalies"]})
        self.assertIsNone(row["hubspot_id"])

    def test_reponse_inversee_de_l_essai_4_remise_a_l_endroit(self):
        # Réponse réelle de l'IA n°1 lors de l'essai du 18/11 : clé = ancienne propriété HubSpot.
        self.break_skill(job_title="jobtitle_ancien")
        inverted = {**FIX_JOBTITLE, "mapping": {"jobtitle_ancien": "jobtitle"}}
        hs = FakeHubSpot()
        row = self.run_one(SAMPLE[0], hs, fake_chat(inverted, APPROVE))
        self.assertEqual(row["self_heal"]["result"], "envoyée après correction")
        self.assertEqual(sk.load()["mapping"]["job_title"], "jobtitle")
        self.assertNotIn("jobtitle_ancien", sk.load()["mapping"])

    def test_inversion_complete_remise_a_l_endroit(self):
        self.break_skill(job_title="jobtitle_ancien")
        swapped = {**FIX_JOBTITLE, "mapping": {"jobtitle": "job_title"}}
        row = self.run_one(SAMPLE[0], FakeHubSpot(), fake_chat(swapped, APPROVE))
        self.assertEqual(row["self_heal"]["result"], "envoyée après correction")
        self.assertEqual(sk.load()["mapping"]["job_title"], "jobtitle")

    def test_cle_inconnue_toujours_bloquee(self):
        self.break_skill(job_title="jobtitle_ancien")
        unknown = {**FIX_JOBTITLE, "mapping": {"fonction_inventee": "jobtitle"}}
        chat = fake_chat(unknown, APPROVE)
        row = self.run_one(SAMPLE[0], FakeHubSpot(), chat)
        self.assertEqual(row["self_heal"]["result"], "non corrigée")
        self.assertEqual(chat.calls, [1])   # bloquée par les garde-fous, contrôleur pas appelé

    def test_controleur_refuse_la_fiche_reste_en_echec(self):
        self.break_skill(job_title="jobtitle_ancien")
        row = self.run_one(SAMPLE[0], FakeHubSpot(), fake_chat(FIX_JOBTITLE, {"approve": False, "reasons": ["doute"]}))
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["self_heal"]["result"], "non corrigée")
        self.assertEqual(sk.load()["mapping"]["job_title"], "jobtitle_ancien")

    def test_proposition_dangereuse_bloquee_par_les_garde_fous(self):
        self.break_skill(job_title="jobtitle_ancien")
        bad = {**FIX_JOBTITLE, "mapping": {"job_title": "propriete_inventee"}}
        chat = fake_chat(bad, APPROVE)
        row = self.run_one(SAMPLE[0], FakeHubSpot(), chat)
        self.assertEqual(row["self_heal"]["result"], "non corrigée")
        self.assertEqual(chat.calls, [1])              # le contrôleur n'est même pas appelé

    def test_jeton_invalide_pas_de_reparation(self):
        def refuse(props):
            raise HubSpotError(401, "jeton invalide")
        chat = fake_chat(AssertionError("ne doit pas appeler l'IA"))
        row = self.run_one(SAMPLE[0], refuse, chat)
        self.assertEqual(row["status"], "failed")
        self.assertNotIn("self_heal", row)
        self.assertEqual(chat.calls, [])

    def test_limite_de_reparations_par_lancement(self):
        for i in range(heal.MAX_HEALS_PER_RUN):
            heal._count["run-heal"] = i + 1
        r = ORIGINAL_ATTEMPT(HubSpotError(400, "autre erreur"), {}, "run-heal",
                             chat=fake_chat(AssertionError("ne doit pas appeler l'IA")), props=HUBSPOT_PROPS)
        self.assertFalse(r["tried"])
        self.assertIn("limite", r["summary"])


if __name__ == "__main__":
    unittest.main()
