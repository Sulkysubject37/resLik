"""
# ResLik v1.2.1 Behavioral Benchmark
Purpose: Stress-test ResLik under distributional shift.
Non-goals: This is NOT a performance comparison or accuracy benchmark.
"""

"""
Benchmark: Distribution Shift Stress Test.

Hypothesis:
ResLik should react diagnostically to distribution shift.
When applied to a distribution (Target) that differs from the Reference (Source),
ResLik should:
1. Show inflated discrepancy scores.
2. Apply stronger gating (lower gate values).

Metrics:
- Discrepancy Shift: Mean(Disc_Target) - Mean(Disc_Source)
- Gating Attenuation: Mean(Gate_Target) / Mean(Gate_Source)

Failure Condition:
- No diagnostic signal (Discrepancy Shift ~ 0).
- Silent failure (Gating Attenuation ~ 1.0) under strong shift.
"""

import numpy as np
from reslik import ResLikUnit

def run_shift_benchmark():
    print("=== Benchmark: Distribution Shift Stress Test ===")
    
    # Setup
    input_dim = 32
    unit = ResLikUnit(input_dim, 16)
    
    # 1. Source Distribution (Reference)
    # Gaussian(0, 1)
    n_source = 200
    source_data = np.random.normal(0, 1, (n_source, input_dim)).astype(np.float32)
    
    # 2. Target Distribution (Shifted)
    # Gaussian(2, 1.5) -> Covariate Shift
    n_target = 200
    target_data = np.random.normal(2, 1.5, (n_target, input_dim)).astype(np.float32)
    
    # 3. Run ResLik with Source Stats
    print("Running on Source Data (Reference)...")
    _, diag_source = unit(source_data, ref_mean=0.0, ref_std=1.0)
    
    print("Running on Target Data (Shifted)...")
    _, diag_target = unit(target_data, ref_mean=0.0, ref_std=1.0)
    
    # 4. Metrics
    disc_shift = diag_target.max_discrepancy - diag_source.max_discrepancy
    
    # Note: wrapper returns aggregate mean_gate_value
    gate_source = diag_source.mean_gate_value
    gate_target = diag_target.mean_gate_value
    
    gate_attenuation = gate_target / (gate_source + 1e-9)
    
    print(f"Source | Mean Gate: {gate_source:.4f} | Max Disc: {diag_source.max_discrepancy:.4f}")
    print(f"Target | Mean Gate: {gate_target:.4f} | Max Disc: {diag_target.max_discrepancy:.4f}")
    print("-" * 50)
    print(f"Discrepancy Shift (Target - Source): {disc_shift:.4f}")
    print(f"Gating Attenuation (Target / Source): {gate_attenuation:.4f}")
    
    # Validation
    # We expect significant discrepancy shift (> 0) and attenuation (< 1)
    if disc_shift > 1.0 and gate_attenuation < 0.8:
        print("SUCCESS: ResLik correctly identified and gated the shift.")
    else:
        print("FAILURE: ResLik was insensitive to distribution shift.")
        # This is a critical failure for an OOD detection unit.
        exit(1)

if __name__ == "__main__":
    run_shift_benchmark()
