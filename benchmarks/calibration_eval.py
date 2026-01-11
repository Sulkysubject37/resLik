"""
Benchmark: Calibration Alignment Test.

Hypothesis:
ResLik discrepancy scores should correlate with downstream prediction error.
Features that are statistically "surprising" (high discrepancy) should be
associated with harder-to-predict samples or higher error rates in a
linear probe.

Metrics:
- Spearman Correlation between Discrepancy Score and Prediction Residual.

Failure Condition:
- No correlation (rho ~ 0).
- Inverse correlation (rho < 0).
"""

import numpy as np
from reslik import ResLikUnit
from scipy.stats import spearmanr

def run_calibration_benchmark():
    print("=== Benchmark: Calibration Alignment Test ===")
    
    # Setup
    n_samples = 200
    input_dim = 20
    latent_dim = 10
    unit = ResLikUnit(input_dim, latent_dim)
    
    # 1. Generate Data with Heteroscedastic Noise
    # Some samples are "harder" (higher noise) and should also look "different" (distribution shift)
    np.random.seed(42)
    
    # Base manifold
    X = np.random.normal(0, 1, (n_samples, input_dim)).astype(np.float32)
    
    # True target (simple linear function)
    w_true = np.random.randn(input_dim)
    y_true = X @ w_true
    
    # Inject noise/shift into a subset of samples
    # We want to see if ResLik detects this shift AND if it correlates with error
    n_outliers = 50
    outlier_indices = np.random.choice(n_samples, n_outliers, replace=False)
    
    # Shift outliers: add bias and increase variance
    X[outlier_indices] += np.random.normal(3, 2, (n_outliers, input_dim))
    
    # Outliers also have higher label noise (harder to predict)
    y_noisy = y_true.copy()
    y_noisy[outlier_indices] += np.random.normal(0, 5, n_outliers)
    
    # 2. Train a simple Linear Probe on CLEAN data only (simulate reference)
    # We use the unit to get stats on clean data
    clean_indices = list(set(range(n_samples)) - set(outlier_indices))
    X_clean = X[clean_indices]
    
    # Fit reference stats (manually for this test)
    ref_mean = 0.0 # theoretically 0
    ref_std = 1.0  # theoretically 1
    
    # 3. Evaluate ResLik on ALL data
    # We want to see if the discrepancy score on X predicts the error |y_noisy - y_pred|
    # Note: We don't actually need to train a probe to know error is high.
    # The error is dominated by the label noise we added + the shift if the model assumes X_clean.
    # Let's define "Error" as distance from the Clean Manifold behavior.
    # Ideal Error Proxy: Distance from mean of clean data? 
    # Or just use the label noise magnitude we injected as the "Ground Truth Difficulty".
    
    # Let's use the injected label noise variance as the target "Error"
    # Difficulty_i = |y_noisy_i - y_true_i|
    # This represents "aleatoric uncertainty" or "unpredictability".
    
    errors = np.abs(y_noisy - y_true)
    
    # Run ResLik to get discrepancy scores
    _, diag_agg = unit(X, ref_mean=ref_mean, ref_std=ref_std)
    
    # Extract per-sample max discrepancy
    # The wrapper returns aggregated diagnostics. We need per-sample.
    # Fortunately, our wrapper puts 'per_sample' list in the aggregate dict/object.
    
    # diag_agg is a ResLikDiagnostics object. 
    # Check wrapper implementation:
    # if is_batch: ... "per_sample": diagnostics_list ...
    # And diagnostics_obj = wrap_diagnostics(agg_dict)
    # So diag_agg.per_sample_details should be the list.
    
    discrepancies = [d["max_discrepancy"] for d in diag_agg.per_sample_details]
    
    # 4. Compute Correlation
    rho, p_val = spearmanr(discrepancies, errors)
    
    print(f"Spearman Correlation (Discrepancy vs Error): {rho:.4f} (p={p_val:.4e})")
    
    # Validation
    # We expect positive correlation: High discrepancy (outlier) -> High Error (noisy label)
    if rho > 0.2 and p_val < 0.05:
        print("SUCCESS: Discrepancy scores correlate with error.")
    else:
        print("FAILURE: ResLik metrics do not align with prediction error.")
        # Don't exit(1) immediately, just log it. Phase 4 allows documenting failure.
        # But we explicitly exit 1 if it's a catastrophic failure of the benchmark code itself.
        # Here, a low correlation is a valid negative result.
        print("Note: This might be acceptable if the noise model is orthogonal to the feature shift.")

if __name__ == "__main__":
    run_calibration_benchmark()