# Related Paradigms and Positioning

Representation-Level Control Surfaces (RLCS) occupies a unique niche at the intersection of machine learning, control theory, and reliability engineering. This document distinguishes RLCS from related frameworks.

## 1. Selective Prediction / Abstention
*   **Overlap**: Both aim to identify inputs where a model is likely to fail and withhold prediction.
*   **Difference**: Selective prediction typically relies on the model's own output probability (softmax confidence) or a learned "abstention head." RLCS operates *before* the prediction head, assessing the *latent representation* itself.
*   **Position**: RLCS is a mechanism for selective prediction, but it bases the decision on feature consistency rather than output confidence.

## 2. Uncertainty Estimation (Epistemic/Aleatoric)
*   **Overlap**: Both quantify doubt about an input.
*   **Difference**: Uncertainty estimation (e.g., Bayesian NN, Ensembles) tries to model the full posterior distribution of parameters or data. This is often computationally expensive (sampling, multiple forward passes). RLCS provides a lightweight, deterministic *proxy* for epistemic uncertainty (out-of-distribution detection) via residual discrepancy.
*   **Position**: RLCS is a low-cost, real-time alternative to full Bayesian uncertainty for runtime control loops.

## 3. Confidence Calibration
*   **Overlap**: Both seek to align model scores with true correctness.
*   **Difference**: Calibration (e.g., Platt scaling) adjusts the *output* probability after processing. RLCS intervenes at the *input* (feature) level. A calibrated model can still confidently predict nonsense on OOD data; RLCS detects the OOD nature directly.
*   **Position**: RLCS is complementary to calibration. Calibration fixes the score; RLCS validates the evidence.

## 4. Runtime Monitoring / OOD Detection
*   **Overlap**: Both detect anomalies during deployment.
*   **Difference**: Monitors are often passive observers that log alerts to a dashboard. RLCS is designed as a *control surface*—it emits structured signals intended for immediate automated consumption by a downstream controller, not just a human analyst.
*   **Position**: RLCS is "active monitoring" wired directly into the execution graph.

## 5. Control Theory (Sensors vs. Controllers)
*   **Overlap**: RLCS adopts the strict separation of sensing and actuation from classical control.
*   **Difference**: Classical sensors measure physical quantities (temperature, velocity). RLCS sensors measure *informational* quantities (representation likelihood, manifold distance).
*   **Position**: RLCS extends the concept of a "virtual sensor" to the latent spaces of deep learning models.

## Summary: Why RLCS is Not Rebranding
RLCS is not just "uncertainty estimation" because it enforces a control-theoretic architecture (Sensor $\to$ Surface $\to$ Controller). It is not just "OOD detection" because it emphasizes the *gating* and *signaling* interface over the classification of the anomaly. It defines a structural pattern for integrating reliability into autonomous systems.
