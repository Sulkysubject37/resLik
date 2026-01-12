# RLCS Formal System Model

This document provides a system-theoretic abstraction of the Representation-Level Control Surface (RLCS) paradigm.

## 1. State-Flow Model

The data flow in an RLCS-compliant system follows a strict unidirectional path through four distinct functional blocks:

```text
[Environment] 
      | x (raw input)
      v
[Encoder] ---------------------> [Task Head / Downstream]
      | z (representation)               ^
      v                                  |
[RLCS Sensor Array]                      |
      | d (diagnostics)                  |
      v                                  |
[Control Surface]                        |
      | u (control signal)               |
      v                                  |
[External Controller] -------------------+
      | a (action/decision)
      v
[Actuator / System State]
```

### Components

1.  **Encoder ($\mathcal{E}$)**: Maps input $x$ to latent state $z$.
    *   $z = \mathcal{E}(x)$
2.  **RLCS Sensor Array ($\mathcal{S}_{1..k}$)**: A collection of independent sensors mapping latent state $z$ to a composite diagnostic state $d$.
    *   $d = \{ \mathcal{S}_1(z), \mathcal{S}_2(z), \dots \}$
    *   Example: $d = \{ d_{ResLik}, d_{TCS}, d_{Agreement} \}$
3.  **Control Surface ($\Pi$)**: Maps composite diagnostics $d$ to a control recommendation $u$.
    *   $u = \Pi(d)$
4.  **External Controller ($\mathcal{C}$)**: Maps recommendation $u$ and system context $k$ to final action $a$.
    *   $a = \mathcal{C}(u, k)$

## 2. Abstractions

*   **Encoder as State Estimator**: The encoder is treated as a noisy sensor estimating the "true" semantic state of the input.
*   **Sensor as Reliability Functional**: The RLCS sensor evaluates a functional that quantifies the *compatibility* of the estimated state $z$ with the prior expectation (reference manifold).
*   **Surface as Policy Interface**: The control surface exposes a discrete or continuous policy interface (the `ControlAction`) that simplifies the complex, high-dimensional diagnostics into actionable low-dimensional signals.

## 3. System Invariants

To maintain stability and predictability, RLCS systems enforce the following invariants:

1.  **Separation of Optimization**: The parameters of the Encoder ($\mathcal{E}$) and the Sensor ($\mathcal{S}$) are optimized independently. The Sensor does not backpropagate gradients to the Encoder during operation.
2.  **No Goal Definition**: The Control Surface ($\Pi$) has no knowledge of the system's utility function or ultimate goal. It only knows about signal consistency.
3.  **No Direct Actuation**: The output $u$ is strictly informational. The Control Surface cannot modify the Environment or System State directly; it can only request the Controller ($\mathcal{C}$) to do so.
4.  **Deterministic Signaling**: The mapping $\Pi(d) \to u$ is deterministic and stateless. Identical diagnostics must yield identical control signals.
