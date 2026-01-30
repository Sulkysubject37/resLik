# resLIK R Package

This directory contains the R implementation of the Representation-Level Control Surfaces (RLCS) paradigm.

## Overview

The `resLIK` package provides a lightweight, dependency-free (except base R) implementation of the core RLCS sensors and control logic. It is designed to be embedded in R-based AI/ML pipelines (e.g., `torch` for R, `tensorflow` for R, or custom simulations).

## Relationship to Python Implementation

The root of this repository contains the reference Python/C++ implementation (`reslik`). The R package is a **pure R** port of the same mathematical logic. It does **not** bind to the C++ core; it reimplements the vector operations using R's native vectorized arithmetic.

This ensures:
1.  **Ease of installation**: No compilation required.
2.  **Portability**: Runs anywhere R runs.
3.  **Transparency**: The math is visible in R code.

## Installation

You can install the package directly from this subdirectory:

```r
# From the project root
devtools::install("resLIK_package")
```

## Intended Audience

*   **Statisticians**: Who want to verify the distributional properties of the sensors.
*   **R Developers**: Building production ML pipelines in R.
*   **Researchers**: Prototyping control surfaces in R notebooks.

## Documentation

See the package vignette for a conceptual introduction:

```r
vignette("rlcs-introduction", package = "resLIK")
```

## Design Invariants

The `resLIK` package adheres to strict design principles to ensure safety and predictability in AI control systems:

1.  **Sensors are diagnostic, not predictive**: Sensors measure the current state of the representation against a reference. They do not predict future failures or correct the data.
2.  **Control surfaces are deterministic**: Given the same inputs (embeddings and references), the control surface will always yield the same signal. There is no randomness or learning in the decision logic.
3.  **No single sensor can force PROCEED**: The control logic is a "Conservative OR". A `PROCEED` signal is issued only if *all* active sensors agree the state is valid. Any failure triggers `DEFER` or `ABSTAIN`.
4.  **Reference statistics must come from a trusted window**: The `ref_mean` and `ref_sd` parameters in `reslik()` must be derived from a known-good calibration dataset (e.g., a holdout validation set). They should not be updated online during inference.
5.  **Frequent DEFER is expected and conservative**: A `DEFER` signal is not necessarily an error; it indicates uncertainty or slight drift. Systems should be designed to handle frequent deferrals gracefully (e.g., by logging or human review) rather than forcing a decision.

## Control Signal Semantics

The control surface outputs standardized signals that map to specific operational states:

| Signal | Meaning | Recommended System Action |
| :--- | :--- | :--- |
| **PROCEED** | High confidence | Safe to continue with automated processing. |
| **DEFER** | Uncertainty / Drift | Pause execution. Inspect data, request human review, or retry. **Not an error.** |
| **ABSTAIN** | Fundamental Invalidity | Stop processing immediately. Fallback to a safety model or hard-coded default. |

## Integration Patterns

RLCS can be integrated into systems using several architectural patterns:

1.  **Logging-only monitoring**: Run sensors in parallel with your primary model. Log control signals without altering execution. Use this to audit model reliability in production before enabling active control.
2.  **Human-in-the-loop review**: Divert samples that trigger a `DEFER` signal to a human expert for validation. This ensures high-stakes decisions are only automated when the system is confident.
3.  **Encoder redundancy**: Use the `agreement()` sensor to compare embeddings from two different encoders (e.g., a large transformer and a lightweight distilled model). Proceed only when they align.
4.  **Safe fallback model**: When an `ABSTAIN` signal is issued, bypass the complex AI model entirely and use a simple, robust, or hard-coded safety policy to maintain system integrity.
