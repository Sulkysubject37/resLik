import unittest
import sys
from unittest.mock import MagicMock

from reslik.diagnostics import ResLikDiagnostics
from reslik.control_surface import ControlSurface, ControlAction, build_control_signal

class TestControlSurface(unittest.TestCase):
    
    def setUp(self):
        # Default thresholds: high=0.8, low=0.5, max_disc=5.0
        self.cs = ControlSurface(reliability_high=0.8, reliability_low=0.5, max_discrepancy_threshold=5.0)

    def test_proceed_case(self):
        # High reliability, low discrepancy -> PROCEED
        diag = ResLikDiagnostics(mean_gate_value=0.9, max_discrepancy=1.0)
        signal = self.cs.evaluate(diag)
        self.assertEqual(signal.recommended_action, ControlAction.PROCEED)
        self.assertEqual(signal.reliability_score, 0.9)

    def test_downweight_case(self):
        # Medium reliability -> DOWNWEIGHT
        diag = ResLikDiagnostics(mean_gate_value=0.6, max_discrepancy=1.0)
        signal = self.cs.evaluate(diag)
        self.assertEqual(signal.recommended_action, ControlAction.DOWNWEIGHT)

    def test_defer_case(self):
        # Low reliability -> DEFER
        diag = ResLikDiagnostics(mean_gate_value=0.4, max_discrepancy=1.0)
        signal = self.cs.evaluate(diag)
        self.assertEqual(signal.recommended_action, ControlAction.DEFER)

    def test_abstain_case(self):
        # Extreme discrepancy -> ABSTAIN (overrides reliability)
        diag = ResLikDiagnostics(mean_gate_value=0.9, max_discrepancy=10.0)
        signal = self.cs.evaluate(diag)
        self.assertEqual(signal.recommended_action, ControlAction.ABSTAIN)
        
    def test_monotonicity(self):
        # Ensure action severity increases as reliability drops
        scores = [0.9, 0.6, 0.4]
        actions = []
        for s in scores:
            diag = ResLikDiagnostics(mean_gate_value=s, max_discrepancy=1.0)
            actions.append(self.cs.evaluate(diag).recommended_action)
            
        # Expected order: PROCEED (healthiest) -> DOWNWEIGHT -> DEFER (least healthy)
        # Note: Enum order is defined in source, but we check specific values here
        self.assertEqual(actions, [ControlAction.PROCEED, ControlAction.DOWNWEIGHT, ControlAction.DEFER])

    def test_integration_helper(self):
        diag = ResLikDiagnostics(mean_gate_value=0.9, max_discrepancy=1.0)
        # Mock output
        dummy_output = [1, 2, 3]
        signal = build_control_signal(dummy_output, diag, self.cs)
        self.assertEqual(signal.recommended_action, ControlAction.PROCEED)

if __name__ == '__main__':
    unittest.main()
