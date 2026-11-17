"""Tests des mesures, avec un faux journal de migration.

Lancer depuis la racine du dépôt :
  python -m unittest pipeline.metrics.test_compute -v
"""
import json
import unittest
from pathlib import Path

from pipeline.metrics.compute import DEFAULT_TRUTH, compute, load_truth, to_markdown
from pipeline.verification.verify import verify_contact

SAMPLE = json.loads(Path(DEFAULT_TRUTH).read_text(encoding="utf-8"))
TRUTH = load_truth([DEFAULT_TRUTH])


def row(contact, status="success", duration_ms=48000, credits=0.02):
    return {
        "legacy_id": contact["legacy_id"],
        "status": status,
        "extracted": verify_contact(contact)["contact"],
        "duration_ms": duration_ms,
        "credits_used": credits,
    }


class TestMesures(unittest.TestCase):
    def test_migration_parfaite(self):
        m = compute([row(c) for c in SAMPLE], TRUTH)
        self.assertEqual(m["fiches_traitees"], 20)
        self.assertEqual(m["taux_reussite_fiche_pct"], 100.0)
        self.assertEqual(m["taux_fiches_exactes_pct"], 100.0)
        self.assertTrue(all(p == 100.0 for p in m["precision_par_champ_pct"].values()))
        self.assertEqual(m["temps_moyen_s"], 48.0)
        self.assertEqual(m["cout_moyen_par_fiche"], 0.02)
        self.assertEqual(m["extrapolation_3000"]["cout"], 60.0)
        self.assertEqual(m["extrapolation_3000"]["heures_1_agent"], 40.0)

    def test_erreurs_de_lecture_comptees_par_champ(self):
        rows = [row(c) for c in SAMPLE[:4]]
        rows[0]["extracted"]["city"] = "Lille"        # l'agent a mal lu la ville
        rows[1]["extracted"]["phone"] = None           # l'agent n'a pas lu le téléphone
        m = compute(rows, TRUTH)
        self.assertEqual(m["precision_par_champ_pct"]["city"], 75.0)
        self.assertEqual(m["precision_par_champ_pct"]["phone"], 75.0)
        self.assertEqual(m["precision_par_champ_pct"]["email"], 100.0)
        self.assertEqual(m["fiches_100pct_exactes"], 2)

    def test_formats_differents_mais_meme_valeur(self):
        # « 06 39 98 00 01 » et « +33 6 39 98 00 01 » sont le même numéro après nettoyage
        c = dict(SAMPLE[0], phone="06 39 98 00 01", last_name="MOREAU")
        m = compute([row(c)], TRUTH)
        self.assertEqual(m["precision_par_champ_pct"]["phone"], 100.0)
        self.assertEqual(m["precision_par_champ_pct"]["last_name"], 100.0)

    def test_statuts_et_fiches_non_lues(self):
        rows = [row(SAMPLE[0]), row(SAMPLE[1], "partial"), row(SAMPLE[2], "failed"),
                {"legacy_id": "C-0004", "status": "failed", "extracted": None,
                 "duration_ms": None, "credits_used": None}]
        m = compute(rows, TRUTH)
        self.assertEqual(m["envoyees_hubspot"], 2)
        self.assertEqual(m["taux_reussite_fiche_pct"], 50.0)
        self.assertEqual(m["fiches_comparees"], 3)
        self.assertEqual(m["par_statut"], {"success": 1, "partial": 1, "failed": 2})

    def test_journal_vide(self):
        m = compute([], TRUTH)
        self.assertIsNone(m["taux_reussite_fiche_pct"])
        self.assertIn("Fiches traitées | 0", to_markdown(m))


if __name__ == "__main__":
    unittest.main()
