"""Tests de l'envoi vers HubSpot, sans réseau (HubSpot et Supabase sont simulés).

Lancer depuis la racine du dépôt :
  python -m unittest pipeline.hubspot.test_send -v
"""
import json
import unittest
from pathlib import Path

from pipeline.hubspot.send import failed_row, log_status, migrate, migrate_one

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = json.loads((ROOT / "data" / "contacts.sample.json").read_text(encoding="utf-8"))
PIEGES = json.loads((ROOT / "pipeline" / "verification" / "exemples_pieges.json").read_text(encoding="utf-8"))


class FakeHubSpot:
    def __init__(self, fail=False):
        self.sent, self.fail = [], fail

    def __call__(self, props):
        if self.fail:
            raise RuntimeError("HubSpot HTTP 401 : jeton invalide")
        self.sent.extend(props)
        return {p["bascule_legacy_id"]: f"hs-{p['bascule_legacy_id']}" for p in props}


class TestMigrate(unittest.TestCase):
    def test_20_contacts_partent_tous(self):
        hs, log = FakeHubSpot(), []
        rows = migrate(SAMPLE, "run-1", upsert=hs, write_log=log.extend)
        self.assertEqual(len(rows), 20)
        self.assertEqual(len(hs.sent), 20)
        self.assertTrue(all(r["status"] == "success" for r in rows))
        self.assertEqual(rows[0]["hubspot_id"], "hs-C-0001")
        self.assertEqual(log, rows)
        self.assertEqual(hs.sent[0]["bascule_legacy_id"], "C-0001")
        self.assertEqual(hs.sent[0]["phone"], "+33639980001")

    def test_fiches_bloquees_non_envoyees(self):
        hs = FakeHubSpot()
        rows = migrate(PIEGES, "run-2", upsert=hs, write_log=lambda r: None)
        statuts = {r["legacy_id"]: r["status"] for r in rows}
        self.assertEqual(statuts["C-0001"], "success")
        self.assertEqual(statuts["C-0021"], "duplicate")   # doublon de C-0001
        self.assertEqual(statuts["C-0022"], "failed")      # prénom vide
        self.assertEqual(statuts["C-0023"], "failed")      # e-mail invalide
        self.assertEqual(statuts["C-0024"], "partial")     # à vérifier : envoyée
        envoyes = {p["bascule_legacy_id"] for p in hs.sent}
        self.assertEqual(envoyes, {"C-0001", "C-0024"})
        self.assertIsNone(next(r for r in rows if r["legacy_id"] == "C-0022")["hubspot_id"])

    def test_hubspot_en_panne(self):
        rows = migrate(SAMPLE[:3], "run-3", upsert=FakeHubSpot(fail=True), write_log=lambda r: None)
        self.assertTrue(all(r["status"] == "failed" for r in rows))
        self.assertIn("401", rows[0]["error"])

    def test_simulation_n_envoie_rien(self):
        hs, log = FakeHubSpot(), []
        rows = migrate(SAMPLE[:5], "run-4", dry_run=True, upsert=hs, write_log=log.extend)
        self.assertEqual(hs.sent, [])
        self.assertTrue(all(r["hubspot_id"] is None for r in rows))
        self.assertEqual(len(log), 5)

    def test_mesures_reprises(self):
        rows = migrate(SAMPLE[:1], "run-5", upsert=FakeHubSpot(), write_log=lambda r: None,
                       metrics={"C-0001": {"duration_ms": 48000, "credits_used": 0.02}})
        self.assertEqual(rows[0]["duration_ms"], 48000)
        self.assertEqual(rows[0]["credits_used"], 0.02)

    def test_lignes_conformes_a_migration_log(self):
        rows = migrate(PIEGES, "run-6", upsert=FakeHubSpot(), write_log=lambda r: None)
        colonnes = {"run_id", "legacy_id", "status", "extracted", "anomalies", "hubspot_id",
                    "duration_ms", "credits_used", "error", "agent_session_id", "screenshot_url", "reread",
                    "agent_started_at", "agent_finished_at"}
        for r in rows:
            self.assertEqual(set(r), colonnes)
            self.assertIn(r["status"], {"success", "partial", "failed", "duplicate", "skipped"})


class TestFicheParFiche(unittest.TestCase):
    """migrate_one : chaque fiche est migrée et journalisée dès qu'elle est lue."""

    def test_fiche_envoyee_et_journalisee(self):
        hs, log = FakeHubSpot(), []
        row = migrate_one(SAMPLE[0], "run-7", [], upsert=hs, write_log=log.extend,
                          metrics={"duration_ms": 21000, "credits_used": 0.008})
        self.assertEqual(row["status"], "success")
        self.assertEqual(row["hubspot_id"], "hs-C-0001")
        self.assertEqual(row["duration_ms"], 21000)
        self.assertEqual(log, [row])

    def test_doublon_detecte_au_fil_de_l_eau(self):
        hs = FakeHubSpot()
        doublon = dict(PIEGES[1])               # même e-mail que C-0001 des pièges
        first = PIEGES[0]
        migrate_one(first, "run-8", [], upsert=hs, write_log=lambda r: None)
        row = migrate_one(doublon, "run-8", [first], upsert=hs, write_log=lambda r: None)
        self.assertEqual(row["status"], "duplicate")
        self.assertIsNone(row["hubspot_id"])
        self.assertEqual([p["bascule_legacy_id"] for p in hs.sent], ["C-0001"])

    def test_hubspot_en_panne(self):
        row = migrate_one(SAMPLE[0], "run-9", [], upsert=FakeHubSpot(fail=True), write_log=lambda r: None)
        self.assertEqual(row["status"], "failed")
        self.assertIn("401", row["error"])

    def test_fiche_non_lue_par_l_agent(self):
        row = failed_row("run-10", "C-0042", "session timed_out")
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["error"], "session timed_out")
        self.assertIsNone(row["hubspot_id"])


class TestStatut(unittest.TestCase):
    def test_correspondance(self):
        self.assertEqual(log_status({"status": "ok", "anomalies": []}), "success")
        self.assertEqual(log_status({"status": "warning", "anomalies": []}), "partial")
        self.assertEqual(log_status({"status": "error", "anomalies": [{"code": "duplicate_email"}]}), "duplicate")
        self.assertEqual(log_status({"status": "error", "anomalies": [{"code": "bad_email"}]}), "failed")


if __name__ == "__main__":
    unittest.main()
