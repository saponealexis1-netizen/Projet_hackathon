"""Tests de la vérification.

Lancer depuis la racine du dépôt :
  python -m unittest pipeline.verification.test_verify -v
"""
import json
import unittest
from pathlib import Path

from pipeline.verification.verify import normalize_phone, verify_batch, verify_contact, summarize

ROOT = Path(__file__).resolve().parents[2]


def base(**over):
    c = {
        "legacy_id": "C-0100", "first_name": "Julie", "last_name": "Test",
        "email": "julie.test@exemple.example", "phone": "+33 6 39 98 01 00",
        "company": "Test SARL", "job_title": "Gérante", "city": "Lyon", "notes": None,
    }
    c.update(over)
    return c


def codes(report):
    return {a["code"] for a in report["anomalies"]}


class TestEchantillon(unittest.TestCase):
    def test_les_20_contacts_d_alexis_passent(self):
        contacts = json.loads((ROOT / "data" / "contacts.sample.json").read_text(encoding="utf-8"))
        reports = verify_batch(contacts)
        s = summarize(reports)
        self.assertEqual(s["total"], 20)
        self.assertEqual(s["error"], 0)
        self.assertEqual(s["ready_for_hubspot"], 20)
        self.assertEqual(reports[0]["hubspot"]["phone"], "+33639980001")
        self.assertEqual(reports[0]["hubspot"]["firstname"], "Julien")


class TestTelephone(unittest.TestCase):
    def test_formats_acceptes(self):
        for raw in ["06 39 98 00 01", "06.39.98.00.01", "+33 6 39 98 00 01",
                    "0033 6 39 98 00 01", "+33 (0)6 39 98 00 01", "06-39-98-00-01"]:
            self.assertEqual(normalize_phone(raw), ("+33639980001", None), raw)

    def test_format_refuse(self):
        phone, problem = normalize_phone("06 39 98")
        self.assertIsNotNone(problem)


class TestPieges(unittest.TestCase):
    def test_prenom_vide_bloque(self):
        r = verify_contact(base(first_name="  "))
        self.assertEqual(r["status"], "error")
        self.assertIn("missing_required", codes(r))
        self.assertIsNone(r["hubspot"])

    def test_email_invalide_bloque(self):
        r = verify_contact(base(email="julie.test@exemple"))
        self.assertEqual(r["status"], "error")
        self.assertIn("bad_email", codes(r))

    def test_email_nettoye(self):
        r = verify_contact(base(email=" Julie.Test@Exemple.EXAMPLE "))
        self.assertEqual(r["contact"]["email"], "julie.test@exemple.example")
        self.assertEqual(r["status"], "ok")

    def test_email_absent_avertit(self):
        r = verify_contact(base(email=None))
        self.assertEqual(r["status"], "warning")
        self.assertIn("missing_email", codes(r))

    def test_nom_en_majuscules_corrige(self):
        r = verify_contact(base(last_name="MOREAU", city="saint-étienne"))
        self.assertEqual(r["contact"]["last_name"], "Moreau")
        self.assertEqual(r["contact"]["city"], "Saint-Étienne")
        self.assertEqual(r["status"], "warning")

    def test_identifiant_invalide(self):
        r = verify_contact(base(legacy_id="42"))
        self.assertIn("bad_legacy_id", codes(r))

    def test_champ_invente_par_l_agent(self):
        r = verify_contact(base(age="42"))
        self.assertIn("unknown_field", codes(r))
        self.assertNotIn("age", r["contact"])

    def test_tiret_considere_comme_vide(self):
        r = verify_contact(base(company="-"))
        self.assertIsNone(r["contact"]["company"])
        self.assertIn("missing_optional", codes(r))


class TestDoublons(unittest.TestCase):
    def test_meme_email(self):
        reports = verify_batch([base(), base(legacy_id="C-0101", phone=None,
                                             email="JULIE.TEST@exemple.example")])
        self.assertEqual(reports[0]["status"], "ok")
        self.assertEqual(reports[1]["status"], "error")
        self.assertIn("duplicate_email", codes(reports[1]))

    def test_meme_personne_ecrite_autrement(self):
        reports = verify_batch([
            base(),
            base(legacy_id="C-0101", email="autre@test.example", phone=None,
                 first_name="JULIE", last_name="test", company="Test  SARL"),
        ])
        self.assertIn("duplicate_person", codes(reports[1]))
        self.assertEqual(reports[1]["status"], "warning")

    def test_meme_identifiant(self):
        reports = verify_batch([base(), base(email="x@y.example", phone=None, first_name="Paul")])
        self.assertIn("duplicate_id", codes(reports[1]))


if __name__ == "__main__":
    unittest.main()
