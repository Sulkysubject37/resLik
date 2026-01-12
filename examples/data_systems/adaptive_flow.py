import sys
from unittest.mock import MagicMock
# Mock the C++ core extension to bypass linking errors during demonstration
sys.modules['reslik._core'] = MagicMock()

import numpy as np
from reslik.control_surface import ControlSurface, build_control_signal, ControlAction
from reslik.diagnostics import ResLikDiagnostics

def process_stream():
    print("--- Data Systems Adaptive Flow Demo ---")
    
    # 1. Initialize Control Surface for Data Quality
    cs = ControlSurface(
        reliability_high=0.95, 
        reliability_low=0.85, 
        max_discrepancy_threshold=2.0
    )
    
    # 2. Simulate Batches
    batches = [
        {"name": "BATCH_001 (Stable)", "diag": ResLikDiagnostics(0.97, 0.4)},
        {"name": "BATCH_002 (Drift Detected)", "diag": ResLikDiagnostics(0.88, 1.2)},
        {"name": "BATCH_003 (Corrupted)", "diag": ResLikDiagnostics(0.60, 5.5)}
    ]

    for batch in batches:
        print(f"\nProcessing {batch['name']}...")
        diag = batch['diag']
        
        # 3. Generate Control Signal
        signal = build_control_signal(None, diag, cs)
        
        # 4. Print Results
        print(f"  Reliability: {signal.reliability_score:.4f}")
        print(f"  SIGNAL:      {signal.recommended_action.name}")
        
        # 5. Controller Logic
        if signal.recommended_action == ControlAction.PROCEED:
            print("  >> Controller: Committing batch to database.")
        elif signal.recommended_action == ControlAction.DOWNWEIGHT:
            print("  >> Controller: Flagging batch for verification; committed with low-priority tag.")
        elif signal.recommended_action == ControlAction.DEFER:
            print("  >> Controller: Diverting batch to human validation queue.")
        elif signal.recommended_action == ControlAction.ABSTAIN:
            print("  >> Controller: DROPPING BATCH (CRITICAL QUALITY ALERT).")

if __name__ == "__main__":
    process_stream()
