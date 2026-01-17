# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-01-17

### Consolidated (RLCS v1.0 Paradigm)
This release marks the formal stabilization of the **Representation-Level Control Surfaces (RLCS)** paradigm and includes critical infrastructure and C++ integrity fixes.

### Added
- **Sensor Suite:** Officially accepted **TCS** (Temporal Consistency) and **Agreement Sensor** (Cross-View) as standard RLCS components alongside ResLik.
- **Documentation:** Added canonical **Adoption Guide**, **Sensor Composition Rules**, and domain-specific **Replication Guides** (AI, Robotics, Data Systems).
- **Demos:** Added validated multi-sensor control scenarios demonstrating additive reliability signaling.
- **CI/CD:** Added comprehensive GitHub Actions workflow (C++ unit tests, Python unit tests, simulations).

### Fixed
- **C++ Integrity:** Resolved a critical bug where the C++ core could return zero-size vectors. Enforced latent dimensionality in both C++ and Python wrapper.
- **Build System:** Fixed C++ linking issues (PIC) and upgraded artifact actions to v4.
- **Package Stability:** Standardized internal paths to ensure robust imports during simulation and testing.

### Changed
- **Project Structure:** Reframed repository as the reference implementation of the RLCS paradigm, not just a single algorithm.
- **Terminology:** Standardized terms (Sensing, Signaling, Acting) across all docs.

## [1.1.0-dev] - 2026-01-12

### Changed
- **Project Framing:** Explicitly repositioned ResLik as a **Representation-Level Control Surface**.
- **Documentation:** Added Control Surface Specification (`docs/control_surface.md`) and expanded cross-disciplinary usage guides.
- **Scope Clarification:** Updated non-goals to prevent misuse as a standalone controller or policy learner.

### Added
- **Control Interfaces:** Added `python/reslik/control_policy.py` defining placeholder interfaces for external control logic.
- **Cross-Domain Skeletons:** Added example stubs for Applied AI, Robotics, and Data Systems to demonstrate non-biological integration.

### Note
- **No numerical or behavioral changes from v1.1.0-dev.** The core math and forward-pass logic remain frozen.

## [1.0.0] - 2026-01-12

### Added
- **Core Engine:** Optimized C++ implementation of the Residual Likelihood-Gated Unit (ResLik).
- **Python API:** High-level `ResLikUnit` wrapper with NumPy and optional PyTorch interop.
- **Diagnostics:** Structured `ResLikDiagnostics` providing real-time visibility into gating behavior.
- **Safety Features:** Input validation for NaNs, infinities, and dimension mismatches.
- **Tuning Controls:** Introduced `lambda` (sensitivity) and `tau` (dead-zone) to control over-regularization.
- **Falsification Benchmarks:** Full suite of scripts to verify stability, calibration, and shift detection.

### Fixed
- **Over-regularization:** Mitigated aggressive gating on clean data by implementing the `tau` dead-zone parameter.

### Capabilities (v1.0.0)
- Forward-only inference pass.
- Modality-agnostic representation refinement.
- Per-sample and aggregate diagnostic reporting.

### Limitations
- No autograd support (gradients do not flow through the unit).
- Single-modal reference statistics (assumes unimodal baseline).
- CPU-only numerical core.
