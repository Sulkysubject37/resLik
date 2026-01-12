import sys
from unittest.mock import MagicMock
# Mock the C++ core extension to bypass linking errors during demonstration
sys.modules['reslik._core'] = MagicMock()

import numpy as np
from reslik.control_surface import ControlSurface, build_control_signal, ControlAction
from reslik.diagnostics import ResLikDiagnostics

def perception_loop():
    print("--- Robotics Perception Gating Demo ---")
    
    # 1. Initialize Control Surface for Perception
    # Robotics requires high precision; we use strict thresholds.
    cs = ControlSurface(
        reliability_high=0.90, 
        reliability_low=0.70, 
        max_discrepancy_threshold=3.0
    )
    
    # 2. Simulate Scenarios
    scenarios = [
        {
            "name": "NOMINAL (Clear Weather)",
            "diag": ResLikDiagnostics(mean_gate_value=0.98, max_discrepancy=0.5)
        },
        {
            "name": "MARGINAL (Light Fog)",
            "diag": ResLikDiagnostics(mean_gate_value=0.82, max_discrepancy=2.1)
        },
        {
            "name": "CRITICAL (Sensor Obstruction)",
            "diag": ResLikDiagnostics(mean_gate_value=0.40, max_discrepancy=8.5)
        }
    ]

    for scenario in scenarios:
        print(f"\nScenario: {scenario['name']}")
        
        # In a real system, these would come from ResLikUnit forward pass
        diag = scenario['diag']
        mock_output = np.zeros(10) # Dummy payload
        
        # 3. Generate Control Signal
        signal = build_control_signal(mock_output, diag, cs)
        
        # 4. Print Results
        print(f"  Reliability: {signal.reliability_score:.4f}")
        print(f"  Anomaly:     {signal.max_discrepancy:.4f}")
        print(f"  SIGNAL:      {signal.recommended_action.name}")
        
        # 5. System Execution Flow (Simulated)
        if signal.recommended_action == ControlAction.PROCEED:
            print("  >> System: Full confidence in perception. Proceeding at target velocity.")
        elif signal.recommended_action == ControlAction.DOWNWEIGHT:
            print("  >> System: Marginal inconsistency. Reducing velocity and increasing LIDAR weight.")
        elif signal.recommended_action == ControlAction.DEFER:
            print("  >> System: Reliability drop. Switching to Radar-only localization.")
        elif signal.recommended_action == ControlAction.ABSTAIN:
            print("  >> System: CRITICAL PERCEPTION FAILURE. Engaging emergency braking.")

if __name__ == "__main__":
    perception_loop()
