"""Unit Testing Suite for LC-MS Vision and Bio-Assay ML Verifier."""

import unittest
from src.testing.lc_ms_vision import MassSpecVisionAnalyzer
from src.testing.assay_ml_verifier import BioAssayMLVerifier


class TestTestingModule(unittest.TestCase):
    def setUp(self):
        self.vision = MassSpecVisionAnalyzer()
        self.verifier = BioAssayMLVerifier()

    def test_mass_spec_analysis(self):
        peaks = [45.2, 88.1, 120.4]
        result = self.vision.analyze_spectrum("SMP-001", peaks)
        self.assertIn("purity_score_percent", result)
        self.assertIn("qc_status", result)

    def test_assay_synergy(self):
        result = self.verifier.verify_synergy_and_ic50("Curcumin", "Piperine", 50.0)
        self.assertIn("synergy_index", result)
        self.assertIn("predicted_ic50_uM", result)


if __name__ == "__main__":
    unittest.main()
