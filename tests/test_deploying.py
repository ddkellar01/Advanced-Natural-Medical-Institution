"""Unit Testing Suite for Clinical Deployment & Patient Regimen Generator."""

import unittest
from src.deploying.deploy_protocol import ClinicalDeploymentEngine


class TestDeployingModule(unittest.TestCase):
    def setUp(self):
        self.engine = ClinicalDeploymentEngine()

    def test_protocol_generation(self):
        biomarkers = {"c_reactive_protein": 4.5, "hba1c": 6.2}
        protocol = self.engine.generate_patient_protocol("PT-1001", biomarkers)
        self.assertEqual(protocol["patient_id"], "PT-1001")
        self.assertEqual(protocol["deployment_status"], "ACTIVE")
        self.assertGreater(len(protocol["active_protocol"]), 0)


if __name__ == "__main__":
    unittest.main()
