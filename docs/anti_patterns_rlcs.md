# RLCS Anti-Patterns and Misuse

The strict architectural separation of RLCS is its primary safety feature. Violating this separation leads to fragile, opaque, and unpredictable systems. This document outlines common anti-patterns to avoid.

## 1. The "Shadow Controller" (Treating RLCS as a Controller)
*   **Anti-Pattern**: Programming business logic directly into the RLCS layer (e.g., "If discrepancy > 5, shut down engine").
*   **Why it Fails**: It hides critical decision logic deep in the signal processing stack.
*   **Correction**: RLCS should output `ABSTAIN`. The *Controller* should receive `ABSTAIN` and decide to "shut down engine."

## 2. Dynamic Goal-Seeking (Auto-Tuning Thresholds)
*   **Anti-Pattern**: Dynamically adjusting RLCS thresholds (e.g., `reliability_low`) at runtime to maximize a reward function or accuracy metric.
*   **Why it Fails**: This couples sensing with the objective. The sensor becomes biased, reporting "safe" because it yields a reward, not because the data is actually consistent.
*   **Correction**: Thresholds should be fixed based on statistical validation (e.g., false positive rate), independent of the downstream task reward.

## 3. The "Black Box" Sensor (Hiding Decision Logic)
*   **Anti-Pattern**: The Sensor outputs a discrete decision (`SAFE`/`UNSAFE`) instead of raw diagnostics, hiding the underlying continuous metrics.
*   **Why it Fails**: The Controller loses the ability to perform nuanced fusion (e.g., "Marginally unsafe but redundant sensor is active").
*   **Correction**: The Sensor emits raw diagnostics; the Surface emits signals; the Controller makes decisions.

## 4. Probabilistic Confusion (Equating Reliability with Probability)
*   **Anti-Pattern**: Interpreting the `reliability_score` (gate value) as the probability that the prediction is correct ($P(Y|X)$).
*   **Why it Fails**: A model can be reliably wrong. It can process a "perfect" input (high reliability) and still misclassify it due to poor training.
*   **Correction**: Treat reliability as "Compatibility with Training Distribution," not "Correctness."

## 5. The "Band-Aid" (Using RLCS to Fix Bad Models)
*   **Anti-Pattern**: Using RLCS to aggressively gate features to compensate for a fundamentally broken or under-trained encoder.
*   **Why it Fails**: RLCS is a safety net, not a crutch. If the encoder produces garbage, RLCS will just tell you it's garbage. It cannot magically extract signal where none exists.
*   **Correction**: Fix the encoder first. Use RLCS to monitor its limits.

## 6. Temporal Smoothing (Hiding Volatility)
*   **Anti-Pattern**: Applying a moving average or Kalman filter *inside* the RLCS sensor to make the signal "cleaner."
*   **Why it Fails**: It destroys high-frequency information. A sudden spike might be a critical shock (e.g., collision). Smoothing hides this signal, delaying the controller's reaction.
*   **Correction**: The Sensor emits raw volatility (e.g., TCS Drift). The Controller decides whether to smooth it or react instantly.

