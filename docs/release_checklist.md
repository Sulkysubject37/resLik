# ResLik v1.2.1 Release Checklist

This checklist confirms the state of the repository at the time of the v1.2.1 release.

## What's Included
- [x] **C++ Core:** Numerically stable forward pass with normalization and gating.
- [x] **Python Interface:** Wrapper class with NumPy/PyTorch interop.
- [x] **Diagnostics:** Inspectable discrepancy and gate values.
- [x] **Benchmarks:** Five behavioral tests (Stability, Calibration, Shift, Ablation, Consistency).
- [x] **Documentation:** Theory, Design Choices, Failure Modes, and Benchmark Results.

## Verification Steps Completed
- [x] **Installation:** `pip install .` succeeds in a clean virtual environment.
- [x] **C++ Tests:** All unit tests in `cpp/tests` pass.
- [x] **Python Tests:** All interface and behavioral tests pass.
- [x] **Benchmarks:** All characterization scripts run and match documented behavioral expectations.
- [x] **Reproducibility:** Random seeds verified for consistency.

## Explicit Exclusions
- No autograd/backprop support.
- No GPU acceleration.
- No automated reference statistics estimation (must be provided by user).
- No clinical/biological validation (methodological characterization only).
