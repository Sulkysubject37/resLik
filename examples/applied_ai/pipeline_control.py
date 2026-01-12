import sys
from unittest.mock import MagicMock
# Mock the C++ core extension to bypass linking errors during demonstration
sys.modules['reslik._core'] = MagicMock()

import numpy as np
from reslik.wrapper import ResLikUnit
from reslik.control_surface import ControlSurface, build_control_signal, ControlAction
from reslik.diagnostics import ResLikDiagnostics

def run_pipeline_stage():
    print("--- Applied AI Pipeline Control Demo ---")
    
    # 1. Initialize ResLik and Control Surface
    # For this demo, we use a simple input dimension of 4
    input_dim = 4
    latent_dim = 4
    
    # We'll use a ControlSurface with custom thresholds
    cs = ControlSurface(
        reliability_high=0.85, 
        reliability_low=0.4, 
        max_discrepancy_threshold=4.0
    )
    
    # Detection logic for the demonstration environment
    from reslik import _core
    is_mocked = isinstance(_core, MagicMock)
    
    unit = None
    if not is_mocked:
        try:
            unit = ResLikUnit(input_dim, latent_dim)
        except Exception as e:
            print(f"Note: Could not initialize C++ ResLikUnit ({e}). Using mock diagnostics.")
    else:
        print("Note: C++ core is mocked. Using deterministic mock diagnostics for demonstration.")

    # 2. Simulate Data Batches
    # Batch A: Healthy, consistent data
    batch_a = np.random.normal(0, 1, (10, input_dim)).astype(np.float32)
    
    # Batch B: Anomalous data (high variance/outliers)
    batch_b = np.random.normal(5, 10, (10, input_dim)).astype(np.float32)

    for name, batch in [("HEALTHY BATCH", batch_a), ("ANOMALOUS BATCH", batch_b)]:
        print(f"\nProcessing {name}...")
        
        if unit:
            # Real ResLik forward pass
            gated_out, diag = unit(batch, ref_mean=0.0, ref_std=1.0)
        else:
            # Mock diagnostics for demonstration if C++ core is missing/mocked
            if "HEALTHY" in name:
                diag = ResLikDiagnostics(mean_gate_value=0.92, max_discrepancy=0.8)
                gated_out = batch # Mock output
            else:
                diag = ResLikDiagnostics(mean_gate_value=0.35, max_discrepancy=12.5)
                gated_out = batch * 0.1 # Mock output
        
        # 3. Generate Control Signal
        signal = build_control_signal(gated_out, diag, cs)
        
        # 4. Print Results
        print(f"Reliability Score: {signal.reliability_score:.4f}")
        print(f"Max Discrepancy:  {signal.max_discrepancy:.4f}")
        print(f"RECOMMENDED ACTION: {signal.recommended_action.name}")
        
        # 5. Show how downstream code would branch (Inert Example)
        if signal.recommended_action == ControlAction.PROCEED:
            print(">> System Action: Proceeding with normal inference.")
        elif signal.recommended_action == ControlAction.DOWNWEIGHT:
            print(">> System Action: Reducing influence of this batch in final aggregate.")
        elif signal.recommended_action == ControlAction.DEFER:
            print(">> System Action: ROUTING TO FALLBACK MODEL (Safety Check Triggered).")
        elif signal.recommended_action == ControlAction.ABSTAIN:
            print(">> System Action: CRITICAL FAILURE - Aborting request and logging anomaly.")

if __name__ == "__main__":
    run_pipeline_stage()
