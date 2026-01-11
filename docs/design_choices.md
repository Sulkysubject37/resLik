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
