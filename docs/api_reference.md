# API Reference

This document provides the API reference for the Python interface of `reslik`.

## `reslik.ResLikUnit`

ResLik: Residual Likelihood-Gated Representation Unit.

This unit applies a soft, learned gate to feature embeddings based on their statistical consistency with a reference distribution (e.g., healthy controls). It wraps the optimized C++ implementation.

### Initialization

```python
def __init__(self, input_dim: int, latent_dim: int = 64)
```

**Arguments:**

*   `input_dim` (int): Dimension of the input feature embeddings. Must be positive.
*   `latent_dim` (int): Dimension of the internal projection layer. Must be positive. Default is 64.

### Forward Pass (`__call__`)

```python
def __call__(self, 
             z_in: Union[np.ndarray, Any], 
             ref_mean: float = 0.0, 
             ref_std: float = 1.0, 
             gating_lambda: float = 1.0,
             gating_tau: float = 0.05) -> Tuple[np.ndarray, ResLikDiagnostics]
```

Apply ResLik gating to the input embeddings.

**Arguments:**

*   `z_in` (Union[np.ndarray, torch.Tensor]): Input feature matrix of shape `(n_samples, input_dim)` or vector of shape `(input_dim,)`. If a PyTorch tensor is provided, it is detached and converted to NumPy.
*   `ref_mean` (float): Reference mean for the current feature set. Default is 0.0.
*   `ref_std` (float): Reference standard deviation. Must be > 0. Default is 1.0.
*   `gating_lambda` (float): Sensitivity of the gating mechanism. Higher values mean stricter filtering of outliers. Default is 1.0.
*   `gating_tau` (float): Dead-zone threshold. Discrepancy scores below this value are ignored (gate = 1.0). Helps preserve clean data. Default is 0.05.

**Returns:**

*   `Tuple[np.ndarray, ResLikDiagnostics]`:
    *   Gated output embeddings `(n_samples, latent_dim)` as NumPy array.
    *   Structured `ResLikDiagnostics` object containing gating statistics.

**Raises:**

*   `ValueError`: If dimensions do not match, input contains NaNs/Infs, or parameters are invalid.

---

## `reslik.diagnostics.ResLikDiagnostics`

Structured container for ResLik diagnostic outputs.

### Properties

*   `mean_gate_value` (float): The average gate value applied (0.0 to 1.0). Lower values indicate more suppression (input was inconsistent with reference).
*   `max_discrepancy` (float): The maximum statistical discrepancy observed. Higher values indicate more outlier-like behavior.
*   `per_sample_details` (Optional[List[Dict[str, float]]]): If batch processing, contains details for each sample.

### Methods

#### `to_dict()`

```python
def to_dict(self) -> Dict[str, Any]
```

Convert diagnostics to a standard dictionary.

#### `summary()`

```python
def summary(self) -> str
```

Return a human-readable summary string, e.g.:

```
ResLik Diagnostics:
  Mean Gate Value: 0.8500 (Lower = More Suppression)
  Max Discrepancy: 1.2000 (Higher = More Outlier-ish)
```
