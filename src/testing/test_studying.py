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
        self.assertIn(compounds[0]["name"], "Curcumin")

    def test_compound_screening(self):
        compound_name = "Test Compound"
        smiles = "CC(=O)C=CC=CC1"
        target_receptor = "NF-kB Pathway"
        
        result = self.engine.screen_compound(compound_name, smiles, target_receptor)
        
        self.assertIn("compound_name", result)
        self.assertIn("binding_affinity_kcal_mol", result)
        self.assertIn("result", result)


if __name__ == "__main__":
    unittest.main()
