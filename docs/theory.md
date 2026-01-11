# Theory: The Minimal Res-Lik Unit (MRLU)

## 1. Formal Definition

The **ResLik Unit** transforms an input embedding $z \in \mathbb{R}^d$ into a gated representation $z' \in \mathbb{R}^d$ by modulating features based on their likelihood under an empirical reference distribution.

The transformation follows five steps:

### Step 1: Pre-Normalization
We enforce numerical stability by centering and scaling the input:
$$
\hat{z} = \frac{z - \mu_{batch}}{\sigma_{batch} + \epsilon}
$$
*Note: In inference mode, running statistics are used.*

### Step 2: Shared Feed-Forward Transformation
A shallow non-linear projection captures feature interactions:
$$
h = \sigma(W_1 \hat{z} + b_1)
$$
where $\sigma$ is typically ReLU or GeLU.

### Step 3: Learned Scale
We learn a data-dependent scale factor for each feature dimension:
$$
s = \exp(W_2 h + b_2)
$$
This scale allows the network to dynamically adjust sensitivity.

### Step 4: Discrepancy Calculation
We define a "discrepancy score" $D(z)$ that measures how far the current embedding deviates from expected biological priors (modeled via reference statistics):
$$
D(z)_j = \left| \frac{z_j - \mu_{ref, j}}{\sigma_{ref, j}} \right|
$$

### Step 5: Multiplicative Gating
The final output is the original input modulated by a soft gate derived from the discrepancy and learned scale:
$$
g = \text{sigmoid}(-s \cdot D(z))
$$
$$
z' = z \odot g
$$

## 2. Assumptions
1.  **Reference Statistics exist:** We assume access to a "healthy" or "baseline" distribution to compute $\mu_{ref}$ and $\sigma_{ref}$.
2.  **Feature Independence in Gating:** The discrepancy is calculated element-wise, assuming that extreme deviation in one feature dimension is independently informative (though the learned scale $s$ can capture correlations).
3.  **Unimodality:** The simple discrepancy metric assumes the reference distribution is roughly unimodal. Multimodal distributions may require a mixture-model approach (out of scope for Phase 1).

## 3. Limitations
- **Linear Reference:** The simple Z-score-like discrepancy cannot capture complex manifold deviations.
- **No Causal Mechanism:** The gating purely suppresses "unlikely" values; it does not correct them or infer *why* they are unlikely.