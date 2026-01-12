# Control Surface Specification

This document defines the role of ResLik as a **Representation-Level Control Surface**. It specifies the signals produced, the operational boundaries, and the intended interaction patterns with downstream systems.

## 1. Primary Signals

ResLik units emit three primary diagnostic signals that form the basis for downstream control logic:

| Signal | Type | Description |
| :--- | :--- | :--- |
| **Gate Value** | `float` [0, 1] | A multiplicative coefficient applied to the embedding. Values near 1.0 indicate high consistency; values near 0.0 indicate high suppression. |
| **Discrepancy** | `float` [0, ∞) | A raw measure of statistical deviation from the reference distribution. High values indicate anomalous feature behavior. |
| **Summary Stats** | `object` | Aggregated metrics (e.g., `mean_gate`, `max_discrepancy`) providing a high-level health check of the representation batch. |

## 2. Scope and Boundaries

To maintain its role as a primitive, ResLik adheres to strict operational boundaries:

### What ResLik DOES:
- **Produce Evidence**: It transforms input embeddings into gated outputs and associated diagnostic metadata.
- **Surface Inconsistency**: It highlights features that violate the statistical assumptions of the reference set.
- **Enable Local Gating**: It provides a mechanism to soften the impact of unreliable features before they reach downstream components.

### What ResLik DOES NOT DO:
- **Make Decisions**: ResLik never decides "stop/go" or "true/false." It only provides the numerical evidence.
- **Implement Policies**: It does not contain logic such as "if mean_gate < 0.5, then raise alarm." This logic belongs in external controllers.
- **Learn Tasks**: ResLik is task-agnostic. It does not know if it is helping classify a cell or steer a vehicle.
- **Replace Safety Layers**: While it informs safety, it is not a standalone safety-critical component.

## 3. Downstream Integration Patterns

Systems should consume ResLik signals using explicit, non-learned rules:

1. **Adaptive Routing**: If `max_discrepancy` exceeds a threshold, route the request to a more robust (but more expensive) inference path.
2. **Telemetry and Monitoring**: Pipe `mean_gate` into system dashboards to detect silent data drift in production environments.
3. **Execution Masking**: Use the `gate_value` to mask specific representation subspaces that are currently untrustworthy.
4. **Degraded Performance Modes**: Trigger "Safe Mode" in controllers when the representation-level health signals indicate sustained instability.

## 4. Computational Guarantees

As a control surface, ResLik must be predictable and lightweight:
- **Complexity**: O(N) where N is the feature dimension.
- **Memory**: Constant overhead per unit (proportional to latent dimension).
- **Latency**: Deterministic forward pass with no branching or iterative optimization.
- **Training**: Zero training cost in production (no backpropagation).
