import sys
from unittest.mock import MagicMock
sys.modules['reslik._core'] = MagicMock()

import numpy as np
from reslik.sensors.temporal_consistency import TemporalConsistencySensor
from reslik.diagnostics import ResLikDiagnostics

def run_data_flow():
    print("--- Multi-Sensor Data Ingestion Demo ---")
    
    # 1. Sensors
    tcs = TemporalConsistencySensor(alpha=5.0) # High sensitivity
    
    # 2. Scenario: "Concept Drift" (Slow, Valid Change)
    # ResLik will flag it as OOD. TCS will say it's stable.
    # This combination implies "Valid Novelty", not "Error".
    
    z_t0 = np.array([1.0, 0.0])
    z_t1 = np.array([1.05, 0.05]) # Small step away
    
    tcs.update(z_t0)
    metrics_tcs = tcs.update(z_t1)
    
    # Mock ResLik: Says OOD because it's far from training mean (0,0)
    reslik_score = 0.3
    
    print("\nEvent: New Market Trend (Valid Drift)...")
    print(f"[ResLik] Population Fit: {reslik_score:.2f} (OOD - Novelty)")
    print(f"[TCS]    Evolution:      {metrics_tcs['temporal_consistency']:.2f} (Stable - Consistent)")
    
    # 3. Control Decision
    # ResLik Low + TCS High = "New Normal" -> ADAPT / LOG
    # ResLik Low + TCS Low  = "Broken Data" -> REJECT
    
    if reslik_score < 0.5 and metrics_tcs['temporal_consistency'] > 0.8:
        print("\n[Control] Action: PROCEED_WITH_TAG")
        print(">>")
        print("Logic: Data is OOD but evolving stably. Likely valid concept drift. Tagging for retraining.")
    elif reslik_score < 0.5:
        print("\n[Control] Action: REJECT")
        print(">>")
        print("Logic: Data is OOD and unstable. Garbage.")

if __name__ == "__main__":
    run_data_flow()
