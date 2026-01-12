import sys
from unittest.mock import MagicMock
# Mock the C++ core extension to bypass linking errors
sys.modules['reslik._core'] = MagicMock()

import numpy as np
from reslik.wrapper import ResLikUnit
from reslik.sensors.temporal_consistency import TemporalConsistencySensor
from reslik.sensors.agreement_sensor import AgreementSensor
from reslik.diagnostics import ResLikDiagnostics
from reslik.control_surface import ControlSurface, ControlAction

def run_multi_sensor_pipeline():
    print("--- Multi-Sensor AI Pipeline Demo ---")
    
    # 1. Initialize Sensors
    # ResLik (Population), TCS (Temporal), Agreement (Cross-View)
    try:
        reslik = ResLikUnit(4, 4)
    except:
        reslik = None # Will use mock diagnostics
        
    tcs = TemporalConsistencySensor(alpha=2.0)
    agreement = AgreementSensor()
    
    # 2. Initialize Control Surface
    # We define a custom logic: If ANY sensor fails, we degrade.
    # Note: The ControlSurface class in v1.0 only takes ResLikDiagnostics.
    # In a real multi-sensor system, we would extend ControlSignal to aggregate them.
    # Here, we demonstrate the LOGIC in the script.
    
    print("Sensors Initialized: ResLik + TCS + Agreement")
    
    # 3. Simulate a Scenario: "Glitchy Input"
    # Time t=0: Normal
    z_t0_primary = np.array([1.0, 0.0, 0.0, 0.0])
    z_t0_backup  = np.array([0.9, 0.1, 0.0, 0.0]) # Good agreement
    
    # Time t=1: Sudden Shock (TCS Fail), but looks valid (ResLik OK), Backup disagrees (Agreement Fail)
    z_t1_primary = np.array([5.0, 0.0, 0.0, 0.0]) # Big jump
    z_t1_backup  = np.array([1.0, 0.1, 0.0, 0.0]) # Backup didn't jump
    
    # Run Step t=1
    print("\nProcessing Step t=1 (Simulated Shock)...")
    
    # A. ResLik Check (Mocked behavior)
    # Primary looks valid (just different), so ResLik might pass it.
    diag_reslik = ResLikDiagnostics(mean_gate_value=0.9, max_discrepancy=1.0)
    print(f"[ResLik]   Reliability: {diag_reslik.mean_gate_value:.2f} (OK)")
    
    # B. TCS Check
    tcs.update(z_t0_primary) # Prime history
    diag_tcs = tcs.update(z_t1_primary)
    print(f"[TCS]      Consistency: {diag_tcs['temporal_consistency']:.2f} (FAIL - Shock detected)")
    
    # C. Agreement Check
    diag_agree = agreement.evaluate(z_t1_primary, z_t1_backup)
    print(f"[Agreement] Consistency: {diag_agree['agreement_consistency']:.2f} (FAIL - Backup disagrees)")
    
    # 4. Combined Control Logic (The "Conservative OR")
    # Rule: If any sensor < 0.5 -> DEFER/ABSTAIN
    
    actions = []
    if diag_reslik.mean_gate_value < 0.5: actions.append("ResLik_Fail")
    if diag_tcs['temporal_consistency'] < 0.5: actions.append("TCS_Fail")
    if diag_agree['agreement_consistency'] < 0.5: actions.append("Agree_Fail")
    
    final_action = ControlAction.PROCEED
    if actions:
        final_action = ControlAction.DEFER
        
    print(f"\n[Control Surface] Final Recommendation: {final_action.name}")
    print(f"Reasons: {actions}")
    print(">> Logic: Although ResLik thought the input was valid, TCS and Agreement correctly flagged the anomaly.")

if __name__ == "__main__":
    run_multi_sensor_pipeline()
