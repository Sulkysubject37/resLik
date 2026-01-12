# Theory: The ResLik Sensor Instantiation

## 1. RLCS Sensor Definition

In the context of the Representation-Level Control Surfaces (RLCS) paradigm, **ResLik** implements the **Sensor** layer ($\mathcal{S}$). Its role is to map a latent embedding $z$ to a set of diagnostic metrics and a reliability-weighted representation.

### The Sensing Function $\mathcal{S}(z)$

The sensor transforms an input embedding $z \in \mathbb{R}^d$ into a gated representation $z' \in \mathbb{R}^h$ and diagnostic state $d$ by modulating features based on their consistency with an empirical reference distribution.

The transformation follows five steps:

### Step 1: Pre-Normalization
We enforce numerical stability by centering and scaling the input per-feature:
$$\tilde{z}_i = \frac{z_i - \mu(z_i)}{\sigma(z_i) + \epsilon}$$

### Step 2: Shared Feed-Forward Transformation
A shallow non-linear projection captures feature interactions:
$$f = \text{GELU}(W_1 \tilde{z} + b_1)$$

### Step 3: Learned Scale
We compute a data-dependent scale factor for the sample:
$$s = \text{softplus}(u^\top \tilde{z})$$
$$a = s \cdot f$$

### Step 4: Likelihood-Consistency Discrepancy
We define a "discrepancy score" $C$ that measures how far the current embedding deviates from expected priors (modeled via reference statistics $\mu_{ref}, \sigma_{ref}$):
$$C = \frac{|\text{mean}(z) - \mu_{ref}|}{\sigma_{ref} + \epsilon}$$

### Step 5: Multiplicative Gating (with Dead-Zone)
The final output is the projection $a$ modulated by a soft gate derived from the discrepancy, a sensitivity parameter $\lambda$, and a dead-zone threshold $\tau$:
$$C_{eff} = \max(0, C - \tau)$$
$$g = \exp(-\lambda \cdot C_{eff})$$
$$z' = a \cdot g$$

## 2. From Sensor to Surface

The ResLik sensor outputs two signals required by the RLCS Control Surface:
1.  **Diagnostic State ($d$)**: Derived from $g$ (gate value) and $C$ (discrepancy).
    *   `reliability_score` $\approx \text{mean}(g)$
    *   `max_discrepancy` $= C$
2.  **Gated Representation ($z'$)**: The "safe" payload passed downstream only if the Control Surface recommends `PROCEED`.

## 3. Assumptions
1.  **Reference Statistics exist:** We assume access to a baseline distribution to compute $\mu_{ref}$ and $\sigma_{ref}$.
2.  **Unimodality:** The simple discrepancy metric assumes the reference distribution is roughly unimodal.
3.  **Statelessness:** The sensing function $\mathcal{S}(z)$ depends only on the current input $z$ and frozen parameters.

## 4. Limitations
- **Forward-Only:** This sensor does not support backpropagation through the unit during operation.
- **Linear Reference:** The discrepancy cannot capture complex manifold deviations.
- **No Causal Mechanism:** The gating purely suppresses "unlikely" values; it does not correct them.

