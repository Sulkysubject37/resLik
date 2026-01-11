# Design Choices

## 1. Multiplicative Gating vs. Additive Residuals
Standard ResNets use additive residuals: $y = x + f(x)$. This encourages the network to learn "corrections."
ResLik uses multiplicative gating: $y = x \cdot g(x)$.
**Why?**
In biological data, "noise" often manifests as extreme values or amplification of artifacts. Multiplicative gating allows the model to "silence" or "dampen" specific features that are statistically implausible, effectively acting as a learned, soft feature selector. Additive residuals can accidentally propagate noise.

## 2. Modality-Agnostic Design
ResLik operates on **embeddings** ($\mathbb{R}^d$), not raw data (counts, intensities).
**Why?**
- **Flexibility:** It can be placed after a CNN (imaging), a Transformer (sequences), or a simple MLP (tabular data).
- **Abstraction:** By operating in latent space, we avoid designing custom noise models for every sequencing technology.

## 3. C++ Core + Python Control Plane
**Why?**
- **Performance:** Gating operations on millions of cells/samples require efficient vectorized SIMD instructions.
- **Portability:** A C++ core ensures the logic can be wrapped for R, Julia, or mobile applications in the future.
- **Python Ecosystem:** Data loading and orchestration remain in Python for compatibility with PyTorch/Scanpy/JAX.

## 4. Regularization Sensitivity & Dead-Zone Gating (Phase 4.5 Update)
ResLik introduces two hyperparameters to control its intervention:
- **$\lambda$ (Lambda):** The sensitivity to discrepancy.
- **$\tau$ (Tau):** The dead-zone threshold.

**Why?**
Early benchmarks showed that without a dead-zone ($\tau=0$), ResLik would slightly gate even perfectly clean data due to the natural tails of the Gaussian distribution.
- **$\tau$** defines a "safe zone" (e.g., within 0.8 std devs) where no gating occurs.
- **$\lambda$** defines how aggressively to gate once outside that zone.

**Trade-off:**
Increasing $\tau$ preserves clean data but reduces sensitivity to small noise.
Increasing $\lambda$ crushes outliers but risks over-regularizing valid biological variation.
There is no "perfect" default; it depends on your tolerance for false positives vs. false negatives.