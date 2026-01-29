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
