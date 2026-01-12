# ResLik — A Representation-Level Control Surface (v1.1.0-dev)

ResLik is the first concrete instantiation of the **Representation-Level Control Surfaces (RLCS)** paradigm. It is a modality-agnostic reliability sensor that introduces **likelihood-consistency gating** at the feature level to improve the calibration and stability of data-driven systems.

---

## The RLCS Paradigm

ResLik is the reference implementation of the **Representation-Level Control Surfaces (RLCS)** paradigm. This paradigm describes a class of systems that sense representation reliability and emit control-relevant signals without executing decisions themselves.

- **Sensing (Sensor Array)**: A composable suite of sensors (ResLik, TCS) that quantify different dimensions of representation consistency.
- **Signaling (Control Surface)**: Transforms raw diagnostics into formal recommendations (`PROCEED`, `DOWNWEIGHT`, `DEFER`, `ABSTAIN`) via deterministic, human-interpretable interfaces.
- **Acting (External Controller)**: Downstream systems consume these signals to route data, throttle ingestion, or engage safety fallbacks.

---

## RLCS Sensors (v1.x)

RLCS provides a family of modular sensors that can be mixed and matched based on system requirements:

| Sensor | Type | Senses | Use Case |
| :--- | :--- | :--- | :--- |
| **ResLik** | Population-Level | Deviation from global training manifold | Detecting OOD inputs, novelties, and anomalies. |
| **TCS** | Local Temporal | Deviation from immediate history | Detecting sudden shocks, glitches, and unstable trajectories. |

*Note: Sensors are optional and independent. You can use ResLik alone, TCS alone, or both in parallel feeding a unified Control Surface.*

---

## Important: Release v1.1.0-dev Scope
- **Forward-Only**: Sensors are forward-pass numerical transformations. No autograd support.
- **Stateless & Deterministic**: Signals are derived purely from input state and reference statistics.
- **Non-Executive**: Sensors inform control logic but do not replace the system controller.

---

## Why RLCS Exists

Modern AI pipelines and robotics stacks often suffer from **silent failures** under distribution shift. Features that deviate from training assumptions can lead to overconfident predictions or catastrophic failure modes.

ResLik addresses this by acting as an **evidentiary layer** between representation learning and execution logic, providing cheap, local reliability telemetry at the latent level.

### Cross-Disciplinary Applications
- **Applied AI Pipelines**: Signal when a stage of a multi-model pipeline is processing out-of-distribution features, routing to fallback models or human review.
- **Robotics Perception Stacks**: Provide per-feature confidence to sensor fusion algorithms, allowing graceful degradation when environmental conditions violate assumptions.
- **Data Systems**: Act as a diagnostic gate for streaming data, identifying corruption or drift before it propagates into downstream analytics.

---

## What ResLik Is (and Is Not)

### ✅ What ResLik **is**
- **An RLCS-compliant sensor implementation**
- A **representation-level regularization primitive**
- **Modality-agnostic** (Imaging, Sequencing, Robotics, Finance)
- Designed for **stability, calibration, and diagnostics**

### ❌ What ResLik **is not**
- **Not a Controller**: It does not execute actions or decisions.
- **Not a Policy Learner**: It does not learn "behavior" or optimization goals.
- **Not a Model Fixer**: It cannot extract signals from fundamentally broken encoders.
- **Not Domain-Bound**: While initially validated on biological data, the core math is semantic-neutral.


---

## When NOT to use ResLik
- **During initial model training:** Since v1.0.0 is forward-only, it will break gradients. Use it only at inference or as a post-hoc filter.
- **When absolute signal magnitude is critical:** The multiplicative gating naturally reduces signal magnitude for unusual features.
- **Without proper reference statistics:** If your reference population does not match your expected "normal" state, ResLik will aggressively silence valid data.

---

## Core Idea (High-Level)

Given feature embeddings $z_i \in \mathbb{R}^d$, ResLik:
1. Normalizes embeddings for numerical stability  
2. Applies a shared feed-forward transformation  
3. Learns a **data-dependent scale** per feature  
4. Computes a **normalized discrepancy** from empirical reference statistics  
5. Applies **multiplicative gating** to suppress implausible feature contributions  

Full mathematical details are in [`docs/theory.md`](docs/theory.md).