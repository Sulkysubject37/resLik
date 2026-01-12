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

## 3. Sensing in C++, Signaling in Python
**Why?**
- **Sensing (C++):** Computing discrepancy and gating on millions of samples requires efficient vectorized SIMD instructions. The sensor logic is math-heavy and policy-light, making it ideal for a compiled language.
- **Signaling (Python):** The Control Surface logic is orchestration, not numerics. It must be readable by systems engineers and modifiable without recompiling. Python allows for flexible integration with heterogeneous pipelines (PyTorch, ROS, Airflow).

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

## 5. The RLCS Separation (Sensor vs. Surface)
ResLik enforces a strict architectural boundary between the numerical unit and the control logic.
**Why?**
- **Safety:** The numerical core (Sensor) cannot "decide" to shut down a system. It only reports math. This prevents "smart" bugs where a sensor tries to outsmart the controller.
- **Reusability:** The same C++ Sensor can be used in a robot (requiring millisecond latency) and a batch data pipeline (requiring throughput). Only the Python Surface (policy) changes.
- **Statelessness:** By keeping the Sensor stateless, we ensure that the system is deterministic and easy to debug. A given input $z$ always produces the same signal $u$.