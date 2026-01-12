# RLCS Terminology and Definitions

This document establishes the formal vocabulary for the Representation-Level Control Surfaces (RLCS) paradigm. Precise usage of these terms is required to prevent ambiguity between sensing, learning, and control.

## 1. Core Objects

### Representation
*   **Definition**: A numerical vector ($z$) produced by a transformation function (encoder) that encodes semantic properties of an input.
*   **What it is NOT**: It is not the "truth." It is an estimation subject to noise, bias, and distribution shift.

### Representation Reliability
*   **Definition**: A scalar measure quantifying the statistical consistency of a specific representation instance against a validated reference distribution.
*   **What it is NOT**: It is not "probability of correctness." A representation can be reliable (consistent with training data) but semantically wrong (e.g., a confident misclassification).

### Control Surface
*   **Definition**: The logical boundary where diagnostic measurements are converted into standardized recommendations. It acts as a translation layer between numerical sensing and system policy.
*   **What it is NOT**: It is not a "controller." It does not execute decisions.

## 2. Mechanisms

### Discrepancy
*   **Definition**: The raw statistical distance (e.g., Mahalanobis distance, residual norm) between an input representation and the reference manifold.
*   **What it is NOT**: It is not an "error" term. High discrepancy implies distinctness, which could be an anomaly or a novel discovery depending on context.

### Temporal Consistency
*   **Definition**: A measure of the smoothness/coherence of the representation trajectory over time ($T_t$). High consistency implies stable evolution.
*   **What it is NOT**: It is not "stationarity." A representation can evolve rapidly (low consistency) but validly.

### Drift Score
*   **Definition**: The normalized magnitude of change between consecutive time steps ($D_t$).
*   **What it is NOT**: It is not "concept drift" (which is a long-term population shift). This is immediate, local drift.

### Gating
*   **Definition**: The application of a multiplicative mask to a representation vector, suppressing dimensions that contribute most to high discrepancy.
*   **What it is NOT**: It is not "feature selection" (which is binary and usually static). Gating is continuous and dynamic per sample.

## 3. Operational States

### Sensing vs. Signaling vs. Acting
*   **Sensing**: Measuring physical or virtual properties (e.g., calculating the norm of a vector).
*   **Signaling**: Broadcasting a structured message about that measurement (e.g., emitting a `WARNING` code).
*   **Acting**: Changing the state of the system based on that signal (e.g., shutting down a motor).
*   *Note*: RLCS performs Sensing and Signaling. It never performs Acting.

### Abstention vs. Deferral
*   **Abstention**: A recommendation to *discard* the current input entirely because it violates fundamental validity assumptions (e.g., sensor corruption).
*   **Deferral**: A recommendation to *route* the input to a different processing path (e.g., human-in-the-loop) because the primary path is insufficiently reliable.
*   *Distinction*: Abstention implies invalid data; Deferral implies valid but difficult data.
