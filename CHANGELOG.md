# Changelog

All notable changes to this project will be documented in this file.

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
