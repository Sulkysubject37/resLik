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

## 5. Control vs. Controller

A critical distinction in the ResLik architecture is the separation between providing a **signal** and executing an **action**.

### The Three-Layer Architecture

1.  **Sensing (ResLik Core)**: The C++ numerical unit performs high-speed feature consistency checks. It produces raw diagnostics (gates, discrepancies). It has no concept of what the data represents or what the system is trying to achieve.
2.  **Signaling (Control Surface)**: The Python layer (defined in `reslik.control_surface`) transforms raw diagnostics into formal recommendations (`ControlAction`). It provides a standardized language for downstream systems but does not trigger execution changes.
3.  **Acting (External Controller)**: The parent system (e.g., a robotics stack, a data pipeline, or an AI orchestrator) consumes the `ControlSignal`. It combines this signal with global state (battery levels, safety constraints, business logic) to execute a final decision.

### Why ResLik Does Not Act

ResLik is designed to be **stateless and context-free**. It does not act because:
- **Lack of Authority**: A low-level representation unit should not have the power to shut down a system or override a safety pilot.
- **Lack of Context**: ResLik does not know if a high discrepancy is a critical error or a desired discovery.
- **Independence**: Keeping ResLik separate from the controller allows the same numerical core to be used across vastly different domains (from bio-reactors to autonomous vehicles) by simply changing the external control policy.

