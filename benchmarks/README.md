# ResLik Benchmarks: A Falsification-First Approach

This directory contains scripts designed to stress-test, invalidate, and scope the ResLik method.
Unlike traditional benchmarks that aim to prove superiority, these benchmarks aim to identify:
1. When ResLik fails.
2. Where ResLik adds no value.
3. Whether ResLik's diagnostics correlate with reality.

## Philosophy

> "If a method cannot be falsified, it is not a method."

Our primary metric is **diagnostic utility**, not predictive accuracy.
ResLik is a regularization unit, not a classifier. Therefore, we measure:
- **Stability:** Does it resist noise better than a baseline?
- **Calibration:** Do its "discrepancy scores" actually predict error?
- **Transparency:** Does it fail loudly and informatively under shift?

## Standard Benchmark Template

Every benchmark script in this directory follows this structure:

### 1. Hypothesis
A clear statement of what we expect ResLik to do.
*Example: "ResLik should suppress feature variance when input noise increases."*

### 2. Setup
- **Data:** Synthetic or controlled mock data (no large external datasets).
- **Control:** Baseline model (e.g., identity function, standard scaler).
- **Intervention:** The specific condition being tested (e.g., noise injection, distribution shift).

### 3. Metric
Quantitative measures of success AND failure.
*Example: Cosine similarity drift, Discrepancy-Error correlation.*

### 4. Expected Outcome
What specific result confirms the hypothesis?

### 5. Failure Interpretation
If the benchmark fails (e.g., ResLik performs worse than baseline), what does that mean?
*Example: "If ResLik amplifies noise, the gating mechanism is unstable."*

## Benchmarks included in v1.0.0

The following scripts are used to characterize v1.0.0 behavior:
- `stability_shift.py`: Noise damping characterization.
- `calibration_eval.py`: Discrepancy-error correlation.
- `distribution_shift.py`: OOD detection sensitivity.
- `ablation.py`: Neutrality on clean data.
- `diagnostic_consistency.py`: Mathematical monotonicity check.
- `lambda_sweep.py`: Hyperparameter sensitivity map.

## Reproducibility
- All benchmarks use `np.random.seed(42)` where applicable for deterministic results.
- Benchmarks rely on synthetic Gaussian data; results may vary on heavy-tailed real-world data.
- C++ core uses a fixed deterministic initialization for weights.

## Known Limitations
- **Resolution:** Benchmarks are currently aggregate-focused (mean/max).
- **Modality:** Tested primarily on unimodal Gaussian-like manifolds.
- **Hardware:** CPU-only characterization.
