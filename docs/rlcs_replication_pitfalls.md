# RLCS Replication Pitfalls & Diagnostics

This document lists common ways RLCS implementations fail silently and how to detect them.

## 1. Hidden Fusion (The "Smart" Sensor)
*   **Symptom**: The sensor returns a modified vector `z_new` that is a mix of `z_t` and `z_{t-1}`.
*   **Why it breaks RLCS**: The sensor has become a controller. The downstream system doesn't know the data was modified.
*   **Detection**: Verify the sensor output signature. It should be `Map<String, Float>`, NOT `Vector`.

## 2. Implicit Arbitration (The "Voting" Sensor)
*   **Symptom**: A multi-sensor implementation returns a single "Best Reliability" score by averaging internal metrics.
*   **Why it breaks RLCS**: Hides the specific failure mode (Shock vs OOD).
*   **Detection**: Check if `Agreement` and `ResLik` scores are visible individually in the final log.

## 3. Over-Regularization (The "Blocked" Pipeline)
*   **Symptom**: The system returns `ABSTAIN` for 20%+ of valid traffic.
*   **Cause**: Reference statistics ($\mu, \sigma$) were calculated on a clean subset, but production data is noisy.
*   **Fix**: Increase the Dead-Zone parameter ($\tau$) or re-compute reference stats on a representative sample.

## 4. Debug Checklist for Adopters
- [ ] **Input Check**: Is the input $z$ normalized correctly before reaching the sensor?
- [ ] **Reference Check**: Do the reference statistics match the current encoder version?
- [ ] **Logic Check**: Does the Control Surface return `PROCEED` for a perfect input?
- [ ] **Latency Check**: Is the sensor adding <1ms overhead? (If >10ms, something is wrong).
