# resLik — Representation-Level Control Surfaces (RLCS)
**Version:** v1.2.1

resLik is the **reference implementation** of the *Representation-Level Control Surfaces (RLCS)* paradigm.  
It provides a set of lightweight, forward-only sensors that quantify the reliability of latent representations and expose this information as explicit, control-relevant signals.

RLCS formalizes a missing layer in modern data-driven systems: **representation-level reliability sensing**, decoupled from both learning and execution.

---

## Representation-Level Control Surfaces (RLCS)

RLCS defines a systems architecture in which **reliability is sensed, not learned**, and **signaled, not acted upon**.

The paradigm enforces a strict separation between:
- **Sensing**: measuring consistency properties of representations,
- **Signaling**: mapping measurements to interpretable control signals,
- **Acting**: executing decisions in downstream systems.

RLCS sensors never execute decisions and never embed control logic.  
They exist solely to expose *when* internal representations should be trusted.

---

## RLCS Architecture

An RLCS-compliant system consists of three layers:

1. **Sensing (Sensor Array)**  
   A set of independent, composable sensors that observe latent representations and quantify different failure modes.

2. **Signaling (Control Surface)**  
   A deterministic, stateless interface that maps sensor diagnostics to explicit recommendations  
   (`PROCEED`, `DOWNWEIGHT`, `DEFER`, `ABSTAIN`).

3. **Acting (External Controller)**  
   Application-specific logic that consumes control signals and decides how the system should respond.

This repository implements the sensing and signaling layers only.  
All execution and policy decisions remain external by design.

---

## RLCS Sensors (v1.2.0)

The current release includes three accepted RLCS sensors:

| Sensor | Class | Failure Mode Detected |
|------|------|-----------------------|
| **ResLik** | Population-Level Consistency | Deviation from reference population (out-of-distribution, novelty) |
| **TCS** | Temporal Consistency | Sudden shocks, glitches, or unstable state transitions |
| **Agreement** | Cross-View Consistency | Disagreement between independent representations or modalities |

All sensors are:
- forward-only,
- deterministic,
- interpretable,
- and linear-time in representation size.

Sensors are optional and composable.  
Any subset may be used without altering system semantics.

---

## Design Invariants

The following properties are enforced throughout the implementation:

- **No Learning**: Sensors do not optimize objectives or adapt parameters online.
- **No Backpropagation**: All operations are forward-pass only.
- **No Acting**: Sensors and control surfaces never execute decisions.
- **Deterministic Behavior**: Identical inputs produce identical signals.
- **Composable by Construction**: Sensors operate independently without fusion or arbitration.

Violating these invariants breaks RLCS compliance.

---

## Scope and Intended Use

### Appropriate Use Cases
- Monitoring representation reliability in applied AI pipelines
- Detecting shocks, drift, or conflicts in robotics perception stacks
- Diagnosing data quality issues in streaming or ingestion systems
- Introducing explicit abstention or deferral logic without retraining models

### When *Not* to Use resLik
- During gradient-based training (v1.x is forward-only)
- As a substitute for a controller or policy
- When reference statistics are unavailable or ill-defined
- To repair fundamentally incorrect or unstable encoders

RLCS exposes uncertainty; it does not resolve it.

---

## Documentation Map

This repository is documentation-driven. Key entry points include:

- **[RLCS Adoption Guide](docs/rlcs_adoption_guide.md)** — when and how to use the paradigm
- **[Paradigm Definition](docs/paradigm_rlcs.md)** — formal description of RLCS
- **[Sensor Theory](docs/theory.md)** — mathematical specification of ResLik and companion sensors
- **[Sensor Composition Rules](docs/rlcs_sensor_composition.md)** — how multiple sensors coexist without fusion
- **Replication Guides** — [Applied AI](docs/replication_applied_ai.md), [Robotics](docs/replication_robotics.md), and [Data Systems](docs/replication_data_systems.md)
- **[Multi-Sensor Reports](docs/phase11_multisensor_report.md)** — behavioral validation across domains

All documentation is located under `docs/`.

---

## Repository Scope

This repository provides a **reference implementation** of RLCS for inspection, replication, and controlled integration.

It is intended for:
- system designers evaluating RLCS-style architectures,
- researchers studying representation reliability,
- engineers integrating diagnostic control signals into existing systems.

It is not intended to function as a drop-in safety layer or a turnkey production component.

---

## Installation

The implementation is provided primarily for reference and experimentation.

For local use:
```bash
pip install .
```