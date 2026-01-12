# resLik: Representation-Level Control Surfaces (RLCS)

**Version**: v1.2.0

**resLik** is the reference implementation of the Representation-Level Control Surfaces (RLCS) paradigm. It provides a suite of modular, forward-only sensors designed to monitor the statistical consistency of latent representations in real-time, enabling deterministic control signaling in data-driven systems.

## The RLCS Paradigm

RLCS is a systems architecture that embeds reliability sensing directly into the latent feature spaces of learned models. It rigorously separates the *measurement* of data consistency from the *policy* of execution control.

The architecture enforces a unidirectional flow of information through three distinct layers:

1.  **Sensing (The Sensor Array)**: A composable suite of mathematical functions quantifies specific dimensions of representation consistency (e.g., population likelihood, temporal coherence).
2.  **Signaling (The Control Surface)**: A stateless logic layer maps raw diagnostic metrics to formal, discrete control signals.
3.  **Acting (The External Controller)**: The downstream system consumes control signals to execute decisions (e.g., routing, throttling, fail-safe engagement).

## Repository Scope

This repository serves as the canonical reference for RLCS. It provides:
*   The C++ numerical core for high-performance sensing.
*   Python bindings for integration with PyTorch/NumPy pipelines.
*   Standardized interfaces for the Control Surface and Sensor Array.
*   Reference implementations for three primary sensor types.

## RLCS Sensors (v1.2.0)

The library implements three accepted RLCS sensors, each targeting a distinct failure mode.

| Sensor | Type | Target Failure Mode |
| :--- | :--- | :--- |
| **ResLik** | Population-Level | **Out-of-Distribution (OOD)**: Input deviates from the learned training manifold. |
| **TCS** | Temporal Consistency | **Shock/Glitch**: Input trajectory exhibits physically or statistically impossible discontinuities. |
| **Agreement** | Cross-View | **Modal Conflict**: Independent representations (e.g., Lidar/Camera) disagree on the semantic state. |

## Design Invariants

All components in this repository adhere to the following invariants:

*   **Forward-Only**: Sensors are purely inference-time constructs. They do not support backpropagation or gradient flow.
*   **Stateless Execution**: Output signals are derived strictly from the current input state and frozen reference statistics.
*   **Non-Executive**: Sensors emit information (`ABSTAIN`, `DEFER`) but never execute system-level actions.
*   **Independence**: Sensors operate in parallel and do not fuse representations or arbitration logic.

## Usage Guidelines

**Appropriate Use Cases**
*   Runtime monitoring of latent embeddings in open-world environments.
*   Sensor fusion stacks requiring redundancy validation before integration.
*   High-throughput data ingestion pipelines requiring semantic quality gating.
*   Systems requiring deterministic failure signals from non-deterministic models.

**Inappropriate Use Cases**
*   Attempting to "repair" or "denoise" embeddings (RLCS is a sensor, not a filter).
*   End-to-end training where reliability is part of the loss function.
*   Scenarios requiring representation fusion or modification.

## Documentation

**Primary Documentation**
*   **[RLCS Adoption Guide](docs/rlcs_adoption_guide.md)**: Canonical entry point for system integration.
*   **[Paradigm Definition](docs/paradigm_rlcs.md)**: Formal architectural specification.
*   **[Sensor Composition](docs/rlcs_sensor_composition.md)**: Rules for combining multiple sensors.

**Reference Material**
*   **[ResLik Theory](docs/theory.md)**: Mathematical specification of the Likelihood-Consistency Sensor.
*   **[API Reference](docs/api_reference.md)**: Python interface details.

**Replication Guides**
*   **[Robotics & Cyber-Physical Systems](docs/replication_robotics.md)**
*   **[Applied AI & ML Pipelines](docs/replication_applied_ai.md)**
*   **[Data Systems & Streaming](docs/replication_data_systems.md)**

## Installation

```bash
pip install .
```

## License

MIT
