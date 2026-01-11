# ResLik — Residual Likelihood–Gated Representation Unit (v1.0.0)

ResLik is a **modality-agnostic representation block** for biological data that introduces
**likelihood-consistency gating** at the feature level.  
It is designed to improve **calibration, stability, and interpretability** of learned embeddings
across noisy and heterogeneous omics data.

---

## Important: Release v1.0.0 Scope
ResLik v1.0.0 is a **forward-only numerical transformation**.  
- It is **not end-to-end trainable** in this version (parameters are initialized and can be tuned, but no autograd support is provided).
- It is **not a full model**; it is a **drop-in unit** that can be attached to *any* encoder output.

---

## Why ResLik Exists

Modern bioinformatics pipelines (deep or shallow) often suffer from:
- Overconfident predictions under distribution shift  
- Feature-level noise dominating learned representations  
- Lack of diagnostics explaining *which* features behave unexpectedly  

ResLik addresses these issues by introducing a **residual, likelihood-aware gating mechanism**
that softly penalizes feature embeddings that deviate from empirical biological expectations.

---

## Behavioral Summary (v1.0.0)
Based on falsification-driven benchmarks:
- **Stability under noise ✅**: Effectively dampens representation variance under high feature-level noise.
- **Calibration alignment ✅**: Discrepancy scores correlate strongly with prediction error in synthetic tasks.
- **Distribution shift detection ✅**: Robustly identifies and gates OOD samples via discrepancy inflation.
- **Over-regularization risk ⚠️**: Clean data may be gated slightly (~15%) under default settings. This is mitigated via the `gating_tau` (dead-zone) parameter.

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

---

## When NOT to use ResLik
- **During initial model training:** Since v1.0.0 is forward-only, it will break gradients. Use it only at inference or as a post-hoc filter.
- **When absolute signal magnitude is critical:** The multiplicative gating naturally reduces signal magnitude for unusual features.
- **Without proper reference statistics:** If your reference population does not match your expected "normal" state, ResLik will aggressively silence valid data.

---

## Core Idea (High-Level)

Given feature embeddings $z_i \in \mathbb{R}^d$, ResLik:
1. Normalizes embeddings for numerical stability  
2. Applies a shared feed-forward transformation  
3. Learns a **data-dependent scale** per feature  
4. Computes a **normalized discrepancy** from empirical reference statistics  
5. Applies **multiplicative gating** to suppress implausible feature contributions  

Full mathematical details are in [`docs/theory.md`](docs/theory.md).