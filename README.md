# ResLik — Residual Likelihood–Gated Representation Unit

ResLik is a **modality-agnostic representation block** for biological data that introduces
**likelihood-consistency gating** at the feature level.  
It is designed to improve **calibration, stability, and interpretability** of learned embeddings
across noisy and heterogeneous omics data.

ResLik is **not a full model**.  
It is a **drop-in unit** that can be attached to *any* encoder output.

---

## Why ResLik Exists

Modern bioinformatics pipelines (deep or shallow) often suffer from:

- Overconfident predictions under distribution shift  
- Feature-level noise dominating learned representations  
- Lack of diagnostics explaining *which* features behave unexpectedly  

ResLik addresses these issues by introducing a **residual, likelihood-aware gating mechanism**
that softly penalizes feature embeddings that deviate from empirical biological expectations,
without enforcing hard constraints or modality-specific assumptions.

---

## What ResLik Is (and Is Not)

### ✅ What ResLik **is**
- A **representation-level regularization primitive**
- **Modality-agnostic** (RNA-seq, methylation, proteomics, etc.)
- **Likelihood-aware but likelihood-independent**
- Designed for **stability, calibration, and diagnostics**
- Implemented with a **C++ numerical core** and **Python interface**

### ❌ What ResLik **is not**
- Not a full multi-omics framework  
- Not a disease predictor  
- Not causal  
- Not a pathway discovery method  
- Not a biological mechanism inference tool  

These boundaries are intentional.

---

## Core Idea (High-Level)

Given feature embeddings \( z_i \in \mathbb{R}^d \), ResLik:

1. Normalizes embeddings for numerical stability  
2. Applies a shared feed-forward transformation  
3. Learns a **data-dependent scale** per feature  
4. Computes a **normalized discrepancy** from empirical reference statistics  
5. Applies **multiplicative gating** to suppress implausible feature contributions  

The result is a gated embedding that:
- preserves geometry,
- dampens unstable signals,
- exposes feature-level diagnostics.

Full mathematical details are in [`docs/theory.md`](docs/theory.md).

---

## Repository Structure

```text
reslik/
├── cpp/            # C++ numerical core (no biology, no training logic)
├── python/         # Python wrapper and user-facing API
├── examples/       # Minimal, focused usage examples
├── benchmarks/     # Stability, calibration, and ablation tests
├── docs/           # Theory, design choices, and failure modes
├── CMakeLists.txt
├── pyproject.toml
└── README.md
