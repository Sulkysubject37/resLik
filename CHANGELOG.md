# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-01-12

### Consolidated (RLCS v1.0 Paradigm)
This release marks the formal stabilization of the **Representation-Level Control Surfaces (RLCS)** paradigm. It consolidates all experimental sensors and documentation into a unified, production-ready framework.

### Added
- **Sensor Suite:** Officially accepted **TCS** (Temporal Consistency) and **Agreement Sensor** (Cross-View) as standard RLCS components alongside ResLik.
- **Documentation:** Added canonical **Adoption Guide**, **Sensor Composition Rules**, and domain-specific **Replication Guides** (AI, Robotics, Data Systems).
- **Demos:** Added validated multi-sensor control scenarios demonstrating additive reliability signaling.

### Changed
- **Project Structure:** Reframed repository as the reference implementation of the RLCS paradigm, not just a single algorithm.
- **Terminlogy:** Standardized terms (Sensing, Signaling, Acting) across all docs.

## [1.1.0-dev] - 2026-01-12

### Changed
- **Project Framing:** Explicitly repositioned ResLik as a **Representation-Level Control Surface**.
- **Documentation:** Added Control Surface Specification (`docs/control_surface.md`) and expanded cross-disciplinary usage guides.
- **Scope Clarification:** Updated non-goals to prevent misuse as a standalone controller or policy learner.

### Added
- **Control Interfaces:** Added `python/reslik/control_policy.py` defining placeholder interfaces for external control logic.
- **Cross-Domain Skeletons:** Added example stubs for Applied AI, Robotics, and Data Systems to demonstrate non-biological integration.

### Note
- **No numerical or behavioral changes from v1.0.0.** The core math, C++ engine, and forward-pass logic remain frozen.

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
