import unittest
import numpy as np
import sys
from unittest.mock import MagicMock

from reslik.sensors.temporal_consistency import TemporalConsistencySensor

class TestTemporalConsistencySensor(unittest.TestCase):
    
    def setUp(self):
        self.sensor = TemporalConsistencySensor(alpha=1.0)
        self.start_vec = np.ones(5, dtype=np.float32) # Magnitude sqrt(5) ~ 2.236

    def test_stable_sequence(self):
        """Test 1: Stable Sequence (z_t = z_{t-1} + epsilon)"""
        self.sensor.reset()
        # Initial step
        self.sensor.update(self.start_vec)
        
        # Apply tiny noise
        epsilon = 1e-5
        noisy_vec = self.start_vec + epsilon
        metrics = self.sensor.update(noisy_vec)
        
        # Expect low drift, high consistency
        self.assertLess(metrics['temporal_drift'], 0.01, "Drift should be negligible for stable sequence")
        self.assertGreater(metrics['temporal_consistency'], 0.99, "Consistency should be high for stable sequence")
        
        # Check for oscillation (next step same tiny noise direction)
        noisy_vec_2 = noisy_vec + epsilon
        metrics_2 = self.sensor.update(noisy_vec_2)
        
        # Drift should be similar, not oscillating wildly
        self.assertAlmostEqual(metrics['temporal_drift'], metrics_2['temporal_drift'], places=4)

    def test_gradual_drift(self):
        """Test 2: Gradual Drift (z_t = z_{t-1} + delta, slowly increasing)"""
        self.sensor.reset()
        current_vec = self.start_vec.copy()
        self.sensor.update(current_vec)
        
        drifts = []
        consistencies = []
        
        # Apply increasing perturbations
        deltas = [0.1, 0.2, 0.3, 0.4]
        
        for delta_mag in deltas:
            # Create a perturbation vector of magnitude approx delta_mag * sqrt(5)
            # Actually simplest is to just add scalar delta to all dims
            # perturbation magnitude = sqrt(5 * delta^2)
            perturbation = np.full_like(current_vec, delta_mag)
            
            # Note: We update current_vec purely by adding perturbation to previous state
            # But here we want to test EFFECT of increasing step size.
            # So let's reset sensor each time or carefully construct sequence.
            # The Requirement says: "z_t = z_{t-1} + delta, slowly increasing"
            # This implies the STEP SIZE increases, or the total distance increases?
            # "monotonic increase in D_t" implies the step size (deviation from t-1) increases.
            
            next_vec = current_vec + perturbation
            metrics = self.sensor.update(next_vec)
            
            drifts.append(metrics['temporal_drift'])
            consistencies.append(metrics['temporal_consistency'])
            
            current_vec = next_vec # Update state
            
        # Check monotonicity
        for i in range(len(drifts) - 1):
            self.assertLess(drifts[i], drifts[i+1], f"Drift not monotonic increasing at step {i}")
            self.assertGreater(consistencies[i], consistencies[i+1], f"Consistency not monotonic decreasing at step {i}")

    def test_abrupt_corruption(self):
        """Test 3: Abrupt Corruption (Sudden large jump)"""
        self.sensor.reset()
        self.sensor.update(self.start_vec)
        
        # Massive jump
        jump_vec = self.start_vec * 10.0 # 10x magnitude change
        metrics = self.sensor.update(jump_vec)
        
        # Expect spike in D_t and drop in T_t
        # Diff is 9 * start_vec. Norm diff is 9 * norm(start).
        # D_t = 9 * norm(start) / norm(start) = 9.0
        
        self.assertGreater(metrics['temporal_drift'], 5.0, "Drift should spike on large jump")
        self.assertLess(metrics['temporal_consistency'], 0.1, "Consistency should drop sharply on large jump")

    def test_runtime_sanity(self):
        """Additional check: O(d) runtime (implied) & Scale Invariance check"""
        self.sensor.reset()
        v1 = np.array([1.0, 0.0])
        self.sensor.update(v1)
        metrics_small = self.sensor.update(np.array([2.0, 0.0])) # Jump 1.0 from base 1.0 -> D=1.0
        
        self.sensor.reset()
        v1_big = np.array([1000.0, 0.0])
        self.sensor.update(v1_big)
        metrics_big = self.sensor.update(np.array([2000.0, 0.0])) # Jump 1000.0 from base 1000.0 -> D=1.0
        
        self.assertAlmostEqual(metrics_small['temporal_drift'], metrics_big['temporal_drift'], places=5,
                               msg="Sensor should be scale-invariant due to normalization")

if __name__ == '__main__':
    unittest.main()
