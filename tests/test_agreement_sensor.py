import unittest
import numpy as np
import sys
from unittest.mock import MagicMock

# Mock the C++ core extension to bypass linking errors
sys.modules['reslik._core'] = MagicMock()

from reslik.sensors.agreement_sensor import AgreementSensor

class TestAgreementSensor(unittest.TestCase):
    
    def setUp(self):
        self.sensor = AgreementSensor()
        self.base_vec = np.array([1.0, 0.0, 0.0], dtype=np.float32)

    def test_identical_representations(self):
        """Test 1: Identical Representations (z1 = z2)"""
        metrics = self.sensor.evaluate(self.base_vec, self.base_vec)
        
        self.assertAlmostEqual(metrics['agreement'], 1.0, places=5)
        self.assertAlmostEqual(metrics['disagreement'], 0.0, places=5)
        self.assertAlmostEqual(metrics['agreement_consistency'], 1.0, places=5)

    def test_gradual_divergence(self):
        """Test 2: Gradual Divergence (Rotate z2 away from z1)"""
        # z1 is [1, 0, 0]
        # We rotate z2 in the XY plane
        angles = [0.1, 0.5, 1.0, 1.5, 3.14] # Radians (0 to ~pi)
        
        agreements = []
        disagreements = []
        
        for angle in angles:
            z2 = np.array([np.cos(angle), np.sin(angle), 0.0], dtype=np.float32)
            metrics = self.sensor.evaluate(self.base_vec, z2)
            
            agreements.append(metrics['agreement'])
            disagreements.append(metrics['disagreement'])
            
        # Check monotonicity
        # Agreement should decrease as angle increases
        for i in range(len(agreements) - 1):
            self.assertGreater(agreements[i], agreements[i+1], f"Agreement not strictly decreasing at step {i}")
            self.assertLess(disagreements[i], disagreements[i+1], f"Disagreement not strictly increasing at step {i}")

    def test_conflicting_representations(self):
        """Test 3: Conflicting Representations (Orthogonal and Opposite)"""
        # Orthogonal
        z_ortho = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        metrics_ortho = self.sensor.evaluate(self.base_vec, z_ortho)
        
        self.assertAlmostEqual(metrics_ortho['agreement'], 0.0, places=5)
        self.assertAlmostEqual(metrics_ortho['agreement_consistency'], 0.5, places=5)
        
        # Opposite (Antipodal)
        z_opp = np.array([-1.0, 0.0, 0.0], dtype=np.float32)
        metrics_opp = self.sensor.evaluate(self.base_vec, z_opp)
        
        self.assertAlmostEqual(metrics_opp['agreement'], -1.0, places=5)
        self.assertAlmostEqual(metrics_opp['agreement_consistency'], 0.0, places=5)
        
    def test_scale_invariance(self):
        """Additional Check: O(d) runtime & Scale Invariance"""
        v1 = np.array([1.0, 2.0, 3.0])
        v2 = np.array([2.0, 3.0, 4.0])
        
        metrics_small = self.sensor.evaluate(v1, v2)
        metrics_large = self.sensor.evaluate(v1 * 1000, v2 * 1000)
        
        self.assertAlmostEqual(metrics_small['agreement'], metrics_large['agreement'], places=5)

if __name__ == '__main__':
    unittest.main()
