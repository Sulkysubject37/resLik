"""
Benchmark: Ablation - Over-Regularization Test.

Hypothesis:
If embeddings are already well-behaved (match reference), ResLik should do little.
Ideally, the gating term should be near 1.0, and the output should preserve the
input structure (up to the learned linear projection).

Since the projection (Step 2) is a dense layer, "identity" is defined conceptually
as "minimal gating interference".

Metrics:
- Gating Magnitude: How close is the mean gate to 1.0?
- Distortion Norm (Normalized): ||Output - Input|| / ||Input|| (Proxy, mainly checking scale)

Failure Condition:
- Mean Gate < 0.9 on clean data (Over-gating).
"""

import numpy as np
from reslik import ResLikUnit

def run_ablation_benchmark():
    print("=== Benchmark: Ablation / Over-Regularization ===")
    
    # Setup
    input_dim = 20
    unit = ResLikUnit(input_dim, 10) # Projects to 10 dim
    
    # Clean Data matching reference stats exactly
    n_samples = 100
    clean_data = np.random.normal(0, 1, (n_samples, input_dim)).astype(np.float32)
    
    # Run ResLik with matching stats
    # We set lambda low (0.1) or standard (1.0) to see baseline behavior
    # Ideally at lambda=1.0, clean data (z-score ~ 0-3) should mostly pass.
    
    output, diag = unit(clean_data, ref_mean=0.0, ref_std=1.0, gating_lambda=1.0)
    
    mean_gate = diag.mean_gate_value
    
    print(f"Mean Gate Value on Clean Data: {mean_gate:.4f}")
    
    # Validation
    # A gate of 1.0 is perfect. < 0.9 implies we are throwing away >10% of signal 
    # just because of Gaussian tails.
    
    if mean_gate > 0.9:
        print("SUCCESS: ResLik preserves clean data (minimal over-gating).")
    else:
        print(f"FAILURE: ResLik aggressively gates clean data (Gate={mean_gate:.4f}).")
        print("Consider lowering default lambda or checking softplus initialization.")
        # We don't exit(1) because this is a tuning issue, not a logic bug,
        # but it's important for the benchmark report.

if __name__ == "__main__":
    run_ablation_benchmark()