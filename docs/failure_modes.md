# Failure Modes

This document describes common failure modes and unexpected behaviors when using RLCS sensors.

## Incorrect Reference Statistics
*   **Description**: The `reslik()` sensor produces extremely low gate values (near 0) for data that should be valid, or fails to suppress obvious outliers.
*   **Cause**: This happens when `ref_mean` and `ref_sd` do not accurately represent the target population. If the reference is too narrow, valid data is rejected as OOD. If too broad, outliers are accepted.
*   **Action**: Re-derive reference statistics from a trusted, high-fidelity calibration window. Ensure the calibration data has the same technical characteristics as the inference data.

## Temporal Ordering Violations
*   **Description**: The `tcs()` sensor reports constant `DEFER` signals or nonsensical drift.
*   **Cause**: The sensor assumes that `z_t` and `z_prev` are consecutive steps in a time-series. Passing non-consecutive or shuffled samples breaks this assumption.
*   **Action**: Ensure strict temporal ordering when feeding embeddings to the TCS sensor. For batch processing, ensure the rows correspond to sequential time steps.

## Agreement Sensor Limitations
*   **Description**: Two sensors or models report high agreement (`PROCEED`) but both are incorrect.
*   **Cause**: The agreement sensor measures alignment, not absolute truth. If both sources are compromised by the same failure mode (e.g., common-mode noise), they will agree on an incorrect representation.
*   **Action**: Use independent models or modalities with different technical failure profiles to maximize the benefit of the agreement sensor.

## Why DEFER Dominates in Clean Data
*   **Description**: The system frequently issues `DEFER` even when data appears "clean" to a human observer.
*   **Cause**: RLCS is conservative by design. Minor fluctuations in latent space that exceed default stability thresholds trigger `DEFER`. This is expected behavior to ensure safety in high-stakes environments.
*   **Action**: If the system is too conservative for your use case, tune the thresholds in `rlcs_control()`. However, understand that lowering thresholds reduces the safety margin.
