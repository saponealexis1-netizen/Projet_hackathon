"""Tests de l'orchestration, sans appel réel à H Company (l'agent est simulé).

Lancer depuis la racine du dépôt :
  python -m unittest agent.runner.test_run -v
"""
import unittest
from unittest import mock

from agent.runner import run
from agent.runner.prompts import ANSWER_FORMAT, FIELDS

GOOD = {"legacy_id": "C-0001", "first_name": "Julien", "last_name": "Moreau",
        "email": "julien.moreau@boulangerie-moreau.example.com", "phone": "+33 6 39 98 00 01",
        "company": "Boulangerie Moreau", "job_title": "Gérant", "city": "Lyon",
        "notes": "Commande hebdomadaire de flyers", "error": ""}


def fake_session(answers):
    """Simule create_session + wait : chaque appel renvoie la réponse suivante."""
    calls = {"n": 0, "tasks": []}

    def create(task, fmt, start_url=None, group_id=None, **kw):
        calls["tasks"].append(task)
        calls["n"] += 1
        return f"sess-{calls['n']}"

    def wait(session_id, max_wait_s=600):
        i = int(session_id.split("-")[1]) - 1
        return {"session_id": session_id, "status": "completed", "answer": answers[i],
                "error_code": None, "error": None, "outcome": "success", "steps": 6,
                "cost_usd": 0.004, "duration_ms": 12000, "screenshots": [f"https://shot/{i}.png"]}
    return create, wait, calls


class TestOrchestration(unittest.TestCase):
    def test_format_impose(self):
        self.assertEqual(set(ANSWER_FORMAT["required"]), set(FIELDS) | {"error"})

    def test_lecture_simple(self):
        create, wait, calls = fake_session([GOOD])
        with mock.patch.object(run.hclient, "create_session", create), mock.patch.object(run.hclient, "wait", wait):
            r = run.process("https://crm.example", "C-0001", "run-1", reread=True)
        self.assertEqual(calls["n"], 1)                       # aucune relecture nécessaire
        self.assertEqual(r["contact"]["email"], GOOD["email"])
        self.assertNotIn("error", r["contact"])               # « error » ne part pas dans le contact
        self.assertIn("C-0001", calls["tasks"][0])
        self.assertIn("https://crm.example", calls["tasks"][0])

    def test_relecture_ciblee_D13(self):
        bad = dict(GOOD, email="julien.moreau@boulangerie-moreau")   # e-mail mal lu
        create, wait, calls = fake_session([bad, GOOD])
        with mock.patch.object(run.hclient, "create_session", create), mock.patch.object(run.hclient, "wait", wait):
            r = run.process("https://crm.example", "C-0001", "run-1", reread=True)
        self.assertEqual(calls["n"], 2)                       # l'agent est renvoyé relire
        self.assertIn("e-mail", calls["tasks"][1])
        self.assertEqual(r["reread"]["field"], "email")
        self.assertEqual(r["reread"]["after"], GOOD["email"])
        self.assertAlmostEqual(r["cost_usd"], 0.008)           # coût des deux lectures
        self.assertEqual(len(r["screenshots"]), 2)

    def test_fiche_introuvable(self):
        missing = {f: "" for f in FIELDS} | {"error": "fiche introuvable"}
        create, wait, calls = fake_session([missing])
        with mock.patch.object(run.hclient, "create_session", create), mock.patch.object(run.hclient, "wait", wait):
            r = run.process("https://crm.example", "C-0999", "run-1", reread=True)
        self.assertEqual(calls["n"], 1)                       # pas de relecture si introuvable
        self.assertEqual(r["agent_error"], "fiche introuvable")
        self.assertEqual(r["contact"]["legacy_id"], "C-0999")

    def test_agent_en_panne(self):
        def boom(*a, **k):
            raise RuntimeError("H Company HTTP 429")
        with mock.patch.object(run.hclient, "create_session", boom):
            r = run.process("https://crm.example", "C-0001", "run-1", reread=True)
        self.assertEqual(r["status"], "failed")
        self.assertIn("429", r["error"])


class TestFiletsDeSecurite(unittest.TestCase):
    """Cas réels observés le 17/11 sur l'ancien CRM."""

    def test_fiche_rangee_dans_notes(self):
        import json as _json
        inner = {k: v for k, v in GOOD.items() if k != "error"}
        answer = {f: "" for f in FIELDS} | {"legacy_id": "C-0001", "notes": _json.dumps(inner), "error": "None"}
        contact, error = run.normalize_answer(answer, "C-0001")
        self.assertIsNone(error)
        self.assertEqual(contact["first_name"], "Julien")
        self.assertEqual(contact["notes"], "Commande hebdomadaire de flyers")

    def test_none_en_texte_n_est_pas_une_erreur(self):
        contact, error = run.normalize_answer(dict(GOOD, error="None", notes="null"), "C-0001")
        self.assertIsNone(error)
        self.assertIsNone(contact["notes"])

    def test_autre_fiche_renvoyee(self):
        contact, error = run.normalize_answer(dict(GOOD, legacy_id="C-0002"), "C-0001")
        self.assertIn("C-0002", error)

    def test_reponse_vide(self):
        contact, error = run.normalize_answer({f: "" for f in FIELDS} | {"legacy_id": "C-0001", "error": ""}, "C-0001")
        self.assertEqual(error, "réponse vide")

    def test_pas_de_relecture_si_fiche_vide(self):
        empty = {f: "" for f in FIELDS} | {"legacy_id": "C-0010", "error": ""}
        create, wait, calls = fake_session([empty])
        with mock.patch.object(run.hclient, "create_session", create), mock.patch.object(run.hclient, "wait", wait):
            r = run.process("https://crm.example", "C-0010", "run-1", reread=True)
        self.assertEqual(calls["n"], 1)
        self.assertEqual(r["agent_error"], "réponse vide")


if __name__ == "__main__":
    unittest.main()
