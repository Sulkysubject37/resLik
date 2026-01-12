# RLCS Extension Points and Invariants

The RLCS paradigm is designed to be extensible. While **ResLik** is the reference instantiation, it is not the only possible implementation. This document outlines how new sensors can be developed within the RLCS framework.

## 1. Extension Points

Developers can extend RLCS by substituting the **Sensor** layer with alternative implementations that adhere to the core interface.

### 1.1 Alternative Consistency Metrics
ResLik uses a residual likelihood discrepancy ($C$). Future sensors could implement:
- **Geometry-Aware Sensors**: Utilizing Riemannian manifold distance instead of Euclidean metrics.
- **Density-Based Sensors**: Using Kernel Density Estimation (KDE) or Normalizing Flows for more complex reference distributions.
- **Physics-Informed Sensors**: Incorporating conservation laws or physical constraints directly into the discrepancy calculation.

### 1.2 Differentiable Sensors
An RLCS sensor *may* be differentiable.
- **Use Case**: This allows the "reliability" signal to act as a regularizer during the training of the upstream Encoder.
- **Constraint**: The operational behavior (inference) must remain identical to a non-differentiable sensor. The gradient path is an *augmentation*, not a replacement for the forward-pass logic.

### 1.3 Adaptive Reference Statistics
While ResLik v1.0 uses static reference statistics, extensions could support:
- **Contextual References**: Switching reference statistics based on explicit metadata (e.g., "Day Mode" vs. "Night Mode" stats).
- **Hierarchical References**: Validating consistency against multiple levels of granularity (e.g., "All Cells" -> "Immune Cells" -> "T-Cells").

## 2. Invariants (What Must Not Change)

To remain an RLCS system, any extension must preserve these invariants:

1.  **The "No-Act" Rule**: The extended sensor must typically output diagnostics, never decisions.
2.  **The "Separation" Rule**: The sensor logic must remain distinct from the system controller logic.
3.  **The "Lightweight" Rule**: The complexity of the sensor must not rival the complexity of the encoder. It must remain a "surface," not a "depth."
4.  **The "Frozen Deployment" Rule**: Once deployed, the internal parameters of the sensor (e.g., reference stats) must be frozen to ensure consistent signaling.

## 3. Why ResLik is a Reference
ResLik is the *minimal viable instantiation* of an RLCS sensor. It proves the concept using:
- $O(N)$ complexity.
- No backpropagation requirement.
- Simple Gaussian assumptions.

It serves as a baseline. Extensions are encouraged to trade simplicity for fidelity, provided they respect the architectural boundaries.
