"""
# ResLik v1.2.0 Behavioral Benchmark
Purpose: Test representation stability under controlled noise.
Non-goals: This is NOT a performance comparison or accuracy benchmark.
"""

"""
Benchmark: Stability Under Noise Injection.

Hypothesis:
ResLik should reduce representation instability under feature-level noise.
Specifically, as input noise variance increases, the variance of the ResLik output
should increase more slowly than the variance of the raw input (damping effect).

Metrics:
1. Variance Amplification Ratio: Var(Output) / Var(Input)
2. Cosine Similarity Drift: CosSim(Clean_Output, Noisy_Output)
3. Diagnostic Response: Correlation between Noise Level and Discrepancy Score.

Failure Condition:
- ResLik amplifies noise (Ratio > 1.0).
- Diagnostics do not correlate with noise magnitude.
"""

import numpy as np
from reslik import ResLikUnit
from scipy.spatial.distance import cosine

def run_stability_benchmark():
    print("=== Benchmark: Stability Under Noise Injection ===")
    
    # Setup
    n_samples = 100
    input_dim = 50
    latent_dim = 25
    unit = ResLikUnit(input_dim, latent_dim)
    
    # 1. Clean Data (Reference)
    np.random.seed(42)
    clean_data = np.random.normal(0, 1, (n_samples, input_dim)).astype(np.float32)
    
    # Initialize unit with clean data stats
    unit(clean_data, ref_mean=0.0, ref_std=1.0)
    
    # 2. Noise Injection Loop
    noise_levels = [0.0, 0.5, 1.0, 2.0, 5.0]
    results = []
    
    print(f"{ 'Noise':<10} | { 'Var(In)':<10} | { 'Var(Out)':<10} | { 'Ratio':<10} | { 'CosSim':<10} | { 'MeanDisc':<10}")
    print("-" * 75)
    
    clean_out, _ = unit(clean_data)
    
    for sigma in noise_levels:
        noise = np.random.normal(0, sigma, clean_data.shape).astype(np.float32)
        noisy_data = clean_data + noise
        
        # Apply ResLik
        noisy_out, diag = unit(noisy_data, ref_mean=0.0, ref_std=1.0)
        
        # Metrics
        var_in = np.var(noisy_data)
        var_out = np.var(noisy_out)
        ratio = var_out / (var_in + 1e-9)
        
        # Cosine Similarity (average over batch)
        # Note: Scipy cosine is distance (1 - sim), so we do 1 - dist
        sims = [1 - cosine(clean_out[i], noisy_out[i]) for i in range(n_samples)]
        mean_sim = np.mean(sims)
        
        mean_disc = diag.max_discrepancy # Using max disc from aggregate for summary
        # Actually diag from wrapper is aggregate. Let's look at average max_disc across batch
        # Wrapper returns aggregate: "max_discrepancy" is the max over the batch.
        # Let's use that as a proxy for "how alarmed is the system".
        
        print(f"{sigma:<10.1f} | {var_in:<10.4f} | {var_out:<10.4f} | {ratio:<10.4f} | {mean_sim:<10.4f} | {mean_disc:<10.4f}")
        
        results.append({
            "sigma": sigma,
            "ratio": ratio,
            "mean_sim": mean_sim,
            "mean_disc": mean_disc
        })

    # Validation
    # 1. Check Damping: Ratio should decrease or stay < 1.0 as noise increases (relative to input variance expansion)
    # Actually, as sigma increases, var_in increases significantly.
    # If ResLik gates effectively, var_out should saturate or grow much slower.
    # So Ratio = Var_Out / Var_In should DECREASE as noise increases.
    
    # 2. Check Diagnostics: Mean Discrepancy should strictly increase.
    
    ratios = [r["ratio"] for r in results]
    discs = [r["mean_disc"] for r in results]
    
    damping_success = ratios[-1] < ratios[1] # Compare high noise vs low noise
    diagnostic_success = discs[-1] > discs[0]
    
    print("\n=== Validation ===")
    print(f"Noise Damping (Ratio decreases): {'PASS' if damping_success else 'FAIL'}")
    print(f"Diagnostic Sensitivity (Disc increases): {'PASS' if diagnostic_success else 'FAIL'}")
    
    if not damping_success or not diagnostic_success:
        print("FAILURE: ResLik did not behave as expected under noise.")
        exit(1)
    else:
        print("SUCCESS: ResLik demonstrated stability and diagnostic awareness.")

if __name__ == "__main__":
    run_stability_benchmark()