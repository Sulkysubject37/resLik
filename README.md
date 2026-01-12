# resLik: Representation-Level Control Surfaces (RLCS)

**Current Version**: v1.2.0

**resLik** is the reference implementation of the **Representation-Level Control Surfaces (RLCS)** paradigm. It provides a suite of lightweight, modality-agnostic sensors that monitor the reliability of latent representations in real-time, enabling safer AI and robotics systems.

---

## The Paradigm: What is RLCS?

RLCS is a systems architecture that embeds **reliability sensing** directly into the latent feature spaces of data-driven applications. It separates the *measurement* of data consistency from the *policy* of execution control.

> **Core Principle**: Sensors observe representations and emit signals (e.g., `ABSTAIN`, `DEFER`), but they never execute decisions. Control logic remains external and deterministic.

### The RLCS Stack
1.  **Sensing (The Sensor Array)**: A composable suite of mathematical sensors quantifies consistency (Population, Temporal, Cross-View).
2.  **Signaling (The Control Surface)**: A stateless logic layer maps raw diagnostics to formal, human-interpretable control signals.
3.  **Acting (The External Controller)**: The downstream system consumes these signals to route data, throttle ingestion, or engage safety fallbacks.

---

## The Sensor Suite (v1.2.0)

This repository implements three accepted RLCS sensors:

| Sensor | Type | Target Failure Mode |
| :--- | :--- | :--- |
| **ResLik** | Population-Level | **Out-of-Distribution (OOD)**: Input deviates from the training manifold. |
| **TCS** | Temporal Consistency | **Shock/Glitch**: Input trajectory exhibits impossible jumps or instability. |
| **Agreement** | Cross-View | **Modal Conflict**: Independent sensors (e.g., Lidar/Cam) disagree on the state. |

*All sensors are $O(N)$, forward-only, and require no backpropagation.*

---

## Documentation & Getting Started

### 🏁 Start Here
*   **[RLCS Adoption Guide](docs/rlcs_adoption_guide.md)**: The canonical entry point. Read this to understand if RLCS fits your system.

### Core Concepts
*   **[The RLCS Paradigm](docs/paradigm_rlcs.md)**: Formal definition of the architecture.
*   **[ResLik Theory](docs/theory.md)**: Mathematical specification of the likelihood sensor.
*   **[Sensor Composition](docs/rlcs_sensor_composition.md)**: Rules for combining multiple sensors without fusion.

### Domain-Specific Guides
*   🤖 **[Robotics & Cyber-Physical Systems](docs/replication_robotics.md)**
*   🧠 **[Applied AI & ML Pipelines](docs/replication_applied_ai.md)**
*   📊 **[Data Systems & Streaming](docs/replication_data_systems.md)**

---

## Installation

```bash
pip install .
```

## License
MIT