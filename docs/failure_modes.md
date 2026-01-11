# Failure Modes

ResLik relies on statistical assumptions. When these are violated, it will fail.

## 1. Distribution Shift in Reference
If the "reference" statistics ($\mu_{ref}, \sigma_{ref}$) are computed on a population that is systematically different from the test data (e.g., different age group, different sequencing protocol), ResLik will aggressively gate *everything* as "implausible."
**Symptom:** Output embeddings collapse to near-zero.

## 2. Heavy-Tailed Distributions
Biological data is often heavy-tailed (e.g., power laws). ResLik's Z-score-based discrepancy assumes roughly sub-Gaussian tails.
**Symptom:** Valid biological signals in the tail are consistently suppressed.

## 3. Collapsed Embeddings
If the input encoder produces embeddings where all variation is compressed into a tiny range, the numerical stability term \(\epsilon\) might dominate, rendering the gating random or uniform.
**Symptom:** Gating weights oscillate or saturate at 1.0.

## 4. Adversarial Noise
Noise that perfectly mimics the covariance structure of the reference data but shifts the mean slightly might escape detection.

## 5. Over-Regularization of Clean Data (Phase 4.5)
**Problem:** Even "clean" in-distribution data has variance. Without a dead-zone (\(\tau\)), ResLik will apply a small gating penalty to normal samples (e.g., Gate ~ 0.85 instead of 1.0).
**Mitigation:** Tune `gating_tau`. For standard normal data, \(\tau\) \(\approx\) 0.8 is required to ensure Gate > 0.99.
**Warning:** Setting \(\tau\) too high will make ResLik blind to small noise injections.

## 6. Tuning Sensitivity
ResLik is NOT "set and forget".
- If \(\lambda\) is too high (> 2.0), it behaves like a harsh clamp.
- If \(\lambda\) is too low (< 0.1), it does almost nothing.
- If \(\tau\) is too high (> 1.5), it allows significant noise to pass through.

Users **must** validate the gate distribution on their own hold-out "clean" data to find the right balance.