"""Tests du skill HubSpot, avec de fausses IA (sans réseau).

Lancer depuis la racine du dépôt :
  python -m unittest pipeline.hubspot_skill.test_skill -v
"""
import copy
import json
import unittest

from pipeline.hubspot_skill import llm, skill as sk, update
from pipeline.hubspot_skill.sources import schema_hash

BASE = sk.load()

HUBSPOT_PROPS = [
    {"name": n, "label": n, "type": "string", "fieldType": "text", "readOnly": False, "unique": n == "bascule_legacy_id"}
    for n in ["bascule_legacy_id", "firstname", "lastname", "email", "phone", "company", "jobtitle",
              "city", "bascule_notes", "mobilephone"]
]


def fake_chat(analyst: dict | Exception, reviewer: dict | Exception | None = None):
    """Fausse IA : n°1 renvoie `analyst`, n°2 renvoie `reviewer`. Garde la trace des appels."""
    calls = []

    def chat(n, system, user):
        calls.append(n)
        answer = analyst if n == 1 else reviewer
        if isinstance(answer, Exception):
            raise answer
        return answer

    chat.calls = calls
    return chat


def skill():
    return copy.deepcopy(BASE)


class TestSkillFile(unittest.TestCase):
    def test_skill_de_depart_valide(self):
        self.assertIsNotNone(BASE)
        self.assertEqual(sk.mapping_errors(BASE["mapping"]), [])
        self.assertEqual(sk.current_mapping(), BASE["mapping"])
        self.assertIn(".example", sk.refused_email_tlds())

    def test_markdown_genere(self):
        md = sk.render_markdown(BASE)
        self.assertIn("| `job_title` | `jobtitle` |", md)
        self.assertIn("`.example`", md)

    def test_skill_md_a_jour(self):
        self.assertEqual(sk.SKILL_MD_PATH.read_text(encoding="utf-8"), sk.render_markdown(BASE),
                         "SKILL.md n'est pas à jour : lancer python -m pipeline.hubspot_skill.skill")


class TestGardeFous(unittest.TestCase):
    def test_identifiant_verrouille(self):
        m = {**BASE["mapping"], "legacy_id": "email"}
        self.assertTrue(any("bascule_legacy_id" in e for e in sk.mapping_errors(m)))

    def test_propriete_inexistante(self):
        m = {**BASE["mapping"], "job_title": "poste_inexistant"}
        names = {p["name"] for p in HUBSPOT_PROPS}
        self.assertTrue(any("absentes de HubSpot" in e for e in sk.mapping_errors(m, names)))

    def test_doublon_de_destination(self):
        m = {**BASE["mapping"], "phone": "email"}
        self.assertTrue(any("même propriété" in e for e in sk.mapping_errors(m)))


class TestDeuxIA(unittest.TestCase):
    PROPOSAL = {"summary": "Le téléphone va dans mobilephone", "mapping": {"phone": "mobilephone"},
                "add_refused_email_tlds": [], "known_error": None, "news": [], "alerts": []}

    def test_les_deux_ia_d_accord_applique(self):
        s, chat = skill(), fake_chat(self.PROPOSAL, {"approve": True, "reasons": ["ok"]})
        r = update.propose_and_review(s, "test", "…", {p["name"] for p in HUBSPOT_PROPS}, chat)
        self.assertTrue(r["applied"])
        self.assertEqual(chat.calls, [1, 2])
        self.assertTrue(update.apply(s, r, "test", today="2026-11-18"))
        self.assertEqual(s["mapping"]["phone"], "mobilephone")
        self.assertEqual(s["version"], BASE["version"] + 1)
        self.assertEqual(s["history"][-1]["summary"], "Le téléphone va dans mobilephone")

    def test_controleur_refuse_rien_ne_change(self):
        s, chat = skill(), fake_chat(self.PROPOSAL, {"approve": False, "reasons": ["pas nécessaire"]})
        r = update.propose_and_review(s, "test", "…", None, chat)
        self.assertFalse(r["applied"])
        update.apply(s, r, "test", today="2026-11-18")
        self.assertEqual(s["mapping"], BASE["mapping"])
        self.assertEqual(s["version"], BASE["version"])
        self.assertIn("pas nécessaire", s["alerts"][-1]["message"])

    def test_garde_fous_bloquent_avant_le_controleur(self):
        bad = {**self.PROPOSAL, "mapping": {"legacy_id": "email"}}
        s, chat = skill(), fake_chat(bad, {"approve": True, "reasons": []})
        r = update.propose_and_review(s, "test", "…", None, chat)
        self.assertFalse(r["applied"])
        self.assertEqual(chat.calls, [1], "le contrôleur ne doit même pas être appelé")

    def test_ia_en_panne_rien_ne_casse(self):
        s, chat = skill(), fake_chat(llm.LLMError("HTTP 503"))
        r = update.propose_and_review(s, "test", "…", None, chat)
        self.assertFalse(r["applied"])
        update.apply(s, r, "test")
        self.assertEqual(s["mapping"], BASE["mapping"])

    def test_proposition_vide_rien_a_signaler(self):
        empty = {"summary": "rien à changer", "mapping": {}, "add_refused_email_tlds": [],
                 "known_error": None, "news": [], "alerts": []}
        s, chat = skill(), fake_chat(empty)
        r = update.propose_and_review(s, "test", "…", None, chat)
        self.assertFalse(update.apply(s, r, "test"))
        self.assertEqual(chat.calls, [1])


class TestDeclencheurs(unittest.TestCase):
    def test_champs_premier_passage_sans_ia(self):
        s, chat = skill(), fake_chat(AssertionError("ne doit pas appeler l'IA"))
        changed, msg = update.check_fields(s, HUBSPOT_PROPS, chat)
        self.assertTrue(changed)
        self.assertEqual(s["schema_hash"], schema_hash(HUBSPOT_PROPS))
        self.assertEqual(chat.calls, [])

    def test_champs_inchanges_sans_ia(self):
        s = skill()
        update.check_fields(s, HUBSPOT_PROPS, fake_chat({}))
        chat = fake_chat(AssertionError("ne doit pas appeler l'IA"))
        changed, _ = update.check_fields(s, HUBSPOT_PROPS, chat)
        self.assertFalse(changed)
        self.assertEqual(chat.calls, [])

    def test_propriete_supprimee_dans_hubspot(self):
        s = skill()
        update.check_fields(s, HUBSPOT_PROPS, fake_chat({}))
        props = [p for p in HUBSPOT_PROPS if p["name"] != "jobtitle"] + [
            {"name": "job_function", "label": "Fonction", "type": "string", "fieldType": "text",
             "readOnly": False, "unique": False}]
        proposal = {"summary": "jobtitle a disparu, la fonction va dans job_function",
                    "mapping": {"job_title": "job_function"}, "add_refused_email_tlds": [],
                    "known_error": None, "news": [], "alerts": []}
        chat = fake_chat(proposal, {"approve": True, "reasons": ["jobtitle n'existe plus"]})
        changed, msg = update.check_fields(s, props, chat)
        self.assertTrue(changed)
        self.assertEqual(s["mapping"]["job_title"], "job_function")
        self.assertEqual(s["schema_hash"], schema_hash(props))
        self.assertIn("appliqué", msg)

    def test_erreur_hubspot_apprise(self):
        proposal = {"summary": "HubSpot refuse les e-mails en .test", "mapping": {},
                    "add_refused_email_tlds": [".test"],
                    "known_error": {"message": "Property values were not valid: email", "cause": "domaine .test",
                                    "action": "bloquer les .test à la vérification"},
                    "news": [], "alerts": []}
        s, chat = skill(), fake_chat(proposal, {"approve": True, "reasons": ["cohérent avec l'erreur"]})
        changed, _ = update.learn_from_error(s, "Property values were not valid: email", None, chat)
        self.assertTrue(changed)
        self.assertIn(".test", s["rules"]["refused_email_tlds"])
        self.assertEqual(len(s["known_errors"]), len(BASE["known_errors"]) + 1)

    def test_nouveaute_alerte_sans_toucher_la_correspondance(self):
        proposal = {"summary": "L'API v1 des contacts sera retirée", "mapping": {}, "add_refused_email_tlds": [],
                    "known_error": None,
                    "news": [{"title": "Retrait de l'API Contacts v1", "date": "2026-11-10",
                              "summary": "…", "impact": "alerte"}],
                    "alerts": ["Vérifier que l'envoi utilise bien l'API CRM v3"]}
        s, chat = skill(), fake_chat(proposal, {"approve": True, "reasons": []})
        changed, _ = update.check_news(s, "texte du changelog", chat)
        self.assertTrue(changed)
        self.assertEqual(s["mapping"], BASE["mapping"])
        self.assertEqual(s["hubspot_news"][-1]["impact"], "alerte")
        self.assertIn("API CRM v3", s["alerts"][-1]["message"])


class TestLLM(unittest.TestCase):
    def test_extraction_json_qwen3(self):
        text = '<think>je réfléchis…</think>\n```json\n{"approve": true, "reasons": ["ok"]}\n```'
        self.assertEqual(llm.extract_json(text), {"approve": True, "reasons": ["ok"]})

    def test_reponse_sans_json(self):
        with self.assertRaises(llm.LLMError):
            llm.extract_json("désolé")


if __name__ == "__main__":
    unittest.main()


class TestLLMReseau(unittest.TestCase):
    """Le vrai client HTTP, contre un faux serveur compatible Hugging Face (127.0.0.1)."""

    def setUp(self):
        import threading
        from http.server import BaseHTTPRequestHandler, HTTPServer

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if self.headers.get("Authorization") != "Bearer hf_test":
                    code, obj = 401, {"error": "Invalid credentials"}
                elif body["model"] == "modele/indisponible":
                    code, obj = 400, {"error": "model not supported"}
                else:
                    code, obj = 200, {"choices": [{"message": {"content": '<think>…</think>{"ok": true}'}}]}
                data = json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(data)

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.env = {"SKILL_LLM1_BASE_URL": f"http://127.0.0.1:{self.server.server_port}/v1",
                    "SKILL_LLM1_MODEL": "modele/indisponible", "SKILL_LLM1_FALLBACK_MODELS": "modele/ok",
                    "SKILL_LLM1_API_KEY": "", "no_proxy": "127.0.0.1", "NO_PROXY": "127.0.0.1"}

    def tearDown(self):
        self.server.shutdown()

    def test_modele_de_secours(self):
        from unittest import mock
        with mock.patch.dict("os.environ", {**self.env, "HF_TOKEN": "hf_test"}):
            self.assertEqual(llm.chat_json(1, "s", "u"), {"ok": True})
            self.assertEqual(llm.last_model[1], "modele/ok")

    def test_cle_refusee_message_clair(self):
        from unittest import mock
        with mock.patch.dict("os.environ", {**self.env, "HF_TOKEN": "hf_faux"}):
            with self.assertRaises(llm.LLMError) as ctx:
                llm.chat_json(1, "s", "u")
            self.assertIn("Make calls to Inference Providers", str(ctx.exception))

    def test_secret_vide_ignore(self):
        from unittest import mock
        with mock.patch.dict("os.environ", {"SKILL_LLM2_BASE_URL": "", "SKILL_LLM2_MODEL": ""}):
            cfg = llm.config(2)
            self.assertEqual(cfg["base_url"], llm.HF_ROUTER)
            self.assertEqual(cfg["model"], llm.DEFAULTS[2]["model"])
