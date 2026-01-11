# Benchmark Results

This document records the results of the "Falsification-First" Phase 4 benchmarking campaign.
Benchmarks were run on synthetic data to isolate algorithmic behavior.

## Summary

| Benchmark | Hypothesis | Outcome | Status |
| :--- | :--- | :--- | :--- |
| **Stability Under Noise** | Noise variance amplification should decrease as noise increases. | Ratio dropped from 0.01 to 0.0002. | **PASS** |
| **Calibration Alignment** | Discrepancy scores should correlate with prediction error. | Spearman rho = 0.7354 (p < 1e-35). | **PASS** |
| **Distribution Shift** | Shifted data should trigger high discrepancy and gating. | Discrepancy +2.13, Gating Attenuation 0.16x. | **PASS** |
| **Ablation (Clean Data)** | Clean data should pass through with Gate ~ 1.0. | Mean Gate = 0.8458 (< 0.9 threshold). | **FAIL** |
| **Diagnostic Consistency** | Metrics should be monotonic with deviation. | Strictly monotonic. | **PASS** |

## Detailed Analysis

### 1. Stability Under Noise Injection
**Result:** ResLik effectively dampens noise.
As input noise variance increased from 0.0 to 5.0, the output variance ratio (Out/In) dropped by two orders of magnitude. The system correctly identified the noise as "discrepant" (Mean Disc increased from 0.33 to 3.37) and suppressed it.

### 2. Calibration Alignment
**Result:** Strong correlation with error.
In a synthetic linear probe task with heteroscedastic noise, ResLik's feature-level discrepancy scores correlated strongly (rho=0.73) with the absolute prediction error. This confirms that the "discrepancy" metric is a valid proxy for predictive uncertainty in this setting.

### 3. Distribution Shift Stress Test
**Result:** High sensitivity to shift.
When applied to a shifted Gaussian (Mean 0->2, Std 1->1.5), ResLik reacted aggressively. The mean gate value dropped to 0.1460, effectively silencing 85% of the signal. This behavior is desirable for an OOD safety filter but confirms ResLik is **not** a domain adaptation tool (it suppresses rather than adapts).

### 4. Ablation / Over-Regularization (FAILURE)
**Result:** Aggressive gating on clean data.
Even on "clean" data matching the reference statistics, ResLik applied a mean gate of ~0.85. Ideally, this should be > 0.95.
**Implication:** The default gating sensitivity (`lambda=1.0`) or the learned scale initialization might be too aggressive. Users should be advised to tune `lambda` or treat ResLik as a "conservative" filter that trades some clean signal for safety.

### 5. Diagnostic Consistency
**Result:** Mathematically consistent.
Sweeping a single feature from 0 to 10 produced strictly monotonic increases in discrepancy and decreases in gate value. There are no "dead zones" or non-monotonic artifacts in the response curve.

## Conclusion
ResLik succeeds as a **safety and stability unit**, showing strong resistance to noise and shift. However, it currently fails the **transparency/neutrality** test on clean data, tending to over-regularize. Future work should focus on calibrating the default sensitivity to ensure `Gate ~ 1.0` for in-distribution data.
