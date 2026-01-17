"""
# ResLik v1.2.1 Behavioral Benchmark
Purpose: Verify internal consistency of ResLik signals.
Non-goals: This is NOT a performance comparison or accuracy benchmark.
"""

"""
Benchmark: Diagnostic Consistency Check.

Hypothesis:
Diagnostics should be internally consistent and monotonic.
As we linearly interpolate a sample away from the reference mean,
the discrepancy score should increase monotonically, and the
gate value should decrease monotonically.

Metrics:
- Monotonicity Check (Boolean)

Failure Condition:
- Discrepancy decreases as deviation increases.
- Gate increases as deviation increases.
"""

import numpy as np
from reslik import ResLikUnit

def run_consistency_benchmark():
    print("=== Benchmark: Diagnostic Consistency ===")
    
    input_dim = 10
    unit = ResLikUnit(input_dim, 5)
    
    # Create a trajectory away from the mean
    # Mean = 0. Trajectory: 0 -> 10
    steps = 20
    trajectory = np.linspace(0, 10, steps)
    
    discrepancies = []
    gates = []
    
    print(f"{ 'Deviation':<10} | { 'Discrepancy':<12} | { 'Gate':<10}")
    print("-" * 40)
    
    for val in trajectory:
        # Create input vector with value 'val'
        # To avoid zero-variance issues in normalization (if any), we add tiny noise or just use scalar
        # Wait, standardize_per_feature works on (val - mean)/std. 
        # If vector is constant, std is 0 -> epsilon.
        # Let's use a vector where only ONE dimension moves, others stay at mean (0).
        # This is cleaner.
        
        sample = np.zeros(input_dim, dtype=np.float32)
        sample[0] = val 
        
        # We need to process one by one to get individual diagnostics cleanly via wrapper loop
        # Wrapper handles batch and returns aggregate, but we want precise per-step values.
        # Wrapper's diag object aggregates. But if we pass batch=1, it's exact.
        
        _, diag = unit(sample, ref_mean=0.0, ref_std=1.0)
        
        d_val = diag.max_discrepancy
        g_val = diag.mean_gate_value
        
        discrepancies.append(d_val)
        gates.append(g_val)
        
        print(f"{val:<10.2f} | {d_val:<12.4f} | {g_val:<10.4f}")

    # Check Monotonicity
    # Discrepancy should be non-decreasing
    disc_monotonic = all(x <= y for x, y in zip(discrepancies, discrepancies[1:]))
    
    # Gate should be non-increasing
    gate_monotonic = all(x >= y for x, y in zip(gates, gates[1:]))
    
    print("\n=== Validation ===")
    print(f"Discrepancy Monotonic: {'PASS' if disc_monotonic else 'FAIL'}")
    print(f"Gate Monotonic:        {'PASS' if gate_monotonic else 'FAIL'}")
    
    if disc_monotonic and gate_monotonic:
        print("SUCCESS: Diagnostics behave consistently.")
    else:
        print("FAILURE: Non-monotonic behavior detected.")
        exit(1)

if __name__ == "__main__":
    run_consistency_benchmark()
