# Benchmark Results

This document records the results of the "Falsification-First" Phase 4 and 4.5 benchmarking campaigns.
Benchmarks were run on synthetic data to isolate algorithmic behavior.

## Summary

| Benchmark | Hypothesis | Outcome | Status |
| :--- | :--- | :--- | :--- |
| **Stability Under Noise** | Noise variance amplification should decrease as noise increases. | Ratio dropped from 0.01 to 0.0002. | **PASS** |
| **Calibration Alignment** | Discrepancy scores should correlate with prediction error. | Spearman rho = 0.7354 (p < 1e-35). | **PASS** |
| **Distribution Shift** | Shifted data should trigger high discrepancy and gating. | Discrepancy +2.13, Gating Attenuation 0.16x. | **PASS** |
| **Ablation (Clean Data)** | Clean data should pass through with Gate ~ 1.0. | Mean Gate = 1.0000 (with $\tau=0.8$). | **PASS** |
| **Diagnostic Consistency** | Metrics should be monotonic with deviation. | Strictly monotonic. | **PASS** |

## Detailed Analysis

### 1. Stability Under Noise Injection
**Result:** ResLik effectively dampens noise.
As input noise variance increased from 0.0 to 5.0, the output variance ratio (Out/In) dropped by two orders of magnitude. The system correctly identified the noise as "discrepant" and suppressed it.

### 2. Calibration Alignment
**Result:** Strong correlation with error.
In a synthetic linear probe task with heteroscedastic noise, ResLik's feature-level discrepancy scores correlated strongly (rho=0.73) with the absolute prediction error. This confirms that the "discrepancy" metric is a valid proxy for predictive uncertainty in this setting.

### 3. Distribution Shift Stress Test
**Result:** High sensitivity to shift.
When applied to a shifted Gaussian, ResLik reacted aggressively. The mean gate value dropped to ~0.15, effectively silencing 85% of the signal. This behavior is desirable for an OOD safety filter.

### 4. Ablation / Over-Regularization (Phase 4.5 Update)
**Result:** Resolved via Dead-Zone Gating.
Initial tests (Phase 4) showed aggressive gating on clean data (Gate ~ 0.85). The introduction of the `gating_tau` ($\tau$) parameter in Phase 4.5 allows users to define a "safe zone". With $\tau=0.8$ (matching the expected mean discrepancy of $N(0,1)$ data), clean data passes with a gate of 1.0000.

### 5. Diagnostic Consistency
**Result:** Mathematically consistent.
Sweeping a single feature produced strictly monotonic increases in discrepancy and decreases in gate value.

## Conclusion
ResLik v1.2.1 is a robust **safety and stability unit**. It effectively identifies and suppresses statistical outliers and distribution shifts. While it requires manual tuning of $\lambda$ and $\tau$ to balance sensitivity vs. neutrality, its behavior is predictable, monotonic, and well-characterized.