"""Unit Testing Suite for the Studying Engine & Phytochemical Database."""

import unittest
from src.studying.study_engine import BotanicalDiscoveryEngine
from src.studying.phytochemical_db import PhytochemicalDatabase


class TestStudyingModule(unittest.TestCase):
    def setUp(self):
        self.engine = BotanicalDiscoveryEngine()
        self.db = PhytochemicalDatabase()

    def test_database_retrieval(self):
        compounds = self.db.get_all_compounds()
        self.assertGreater(len(compounds), 0)
        self.assertEqual(compounds[0]["name"], "Curcumin")

    def test_compound_screening(self):
        result = self.engine.screen_compound(
            compound_name="Test Compound",
            smiles="C1=CC=CC=C1",
            target_receptor="NF-kB Pathway"
        )
        self.assertIn("binding_affinity_kcal_mol", result)
        self.assertIn(result["status"], ["VIABLE", "REJECTED"])


if __name__ == "__main__":
    unittest.main()
