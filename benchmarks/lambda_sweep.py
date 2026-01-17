"""
# ResLik v1.2.1 Behavioral Benchmark
Purpose: Add lambda sweep to characterize regularization strength.
Non-goals: This is NOT a performance comparison or accuracy benchmark.
"""

"""
Benchmark: Lambda Sensitivity Sweep.

Hypothesis:
The regularization strength lambda directly controls the trade-off between
preserving clean data (high gate) and suppressing noise (low variance ratio).
We need to characterize this curve to understand the current over-regularization.

Metrics:
- Clean Gate: Mean gate value on clean data (Target ~ 1.0)
- Noise Ratio: Var(Out)/Var(In) on noisy data (Target < 1.0)

Output:
Tabulated sweep results.
"""

import numpy as np
from reslik import ResLikUnit

def run_lambda_sweep():
    print("=== Benchmark: Lambda Sensitivity Sweep ===")
    
    # Setup
    input_dim = 20
    latent_dim = 10
    n_samples = 100
    
    unit = ResLikUnit(input_dim, latent_dim)
    
    # Data
    np.random.seed(42)
    clean_data = np.random.normal(0, 1, (n_samples, input_dim)).astype(np.float32)
    
    # Noisy data for stability check (sigma=2.0)
    noise = np.random.normal(0, 2.0, (n_samples, input_dim)).astype(np.float32)
    noisy_data = clean_data + noise
    var_in_noisy = np.var(noisy_data)
    
    # Sweep
    lambdas = [0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]
    
    print(f"{'Lambda':<10} | {'Clean Gate':<12} | {'Noisy Ratio':<12} | {'Interpretation':<15}")
    print("-" * 65)
    
    for lam in lambdas:
        # 1. Clean Data Pass
        _, diag_clean = unit(clean_data, ref_mean=0.0, ref_std=1.0, gating_lambda=lam)
        clean_gate = diag_clean.mean_gate_value
        
        # 2. Noisy Data Pass
        noisy_out, _ = unit(noisy_data, ref_mean=0.0, ref_std=1.0, gating_lambda=lam)
        var_out_noisy = np.var(noisy_out)
        ratio = var_out_noisy / (var_in_noisy + 1e-9)
        
        interp = ""
        if clean_gate < 0.9:
            interp = "Over-regularized"
        elif ratio > 0.8:
            interp = "Under-regularized"
        else:
            interp = "Balanced-ish"
            
        print(f"{lam:<10.4f} | {clean_gate:<12.4f} | {ratio:<12.4f} | {interp:<15}")

if __name__ == "__main__":
    run_lambda_sweep()
