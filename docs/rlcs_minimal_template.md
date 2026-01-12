# RLCS Minimal Re-Implementation Template

This document provides a language-agnostic template for re-implementing the RLCS paradigm. Use this to port RLCS to C++, Rust, Go, or Java.

## 1. The Sensor Interface

Any RLCS sensor must implement a stateless update/evaluate method that returns raw diagnostics.

```pseudocode
interface RLCSSensor {
    // Input: Latent vector z
    // Output: Dictionary of scalar metrics
    function update(Vector z) -> Map<String, Float>
    
    // Optional: Reset state (for temporal sensors)
    function reset() -> Void
}
```

## 2. The Control Surface Interface

The control surface must be a stateless mapping from diagnostics to a formal signal.

```pseudocode
enum ControlAction {
    PROCEED,
    DOWNWEIGHT,
    DEFER,
    ABSTAIN
}

struct ControlSignal {
    Float reliability_score
    ControlAction action
    Map<String, Float> raw_metrics
}

class ControlSurface {
    // Configurable thresholds
    Float threshold_high
    Float threshold_low
    
    function evaluate(Map<String, Float> diagnostics) -> ControlSignal {
        // 1. Extract primary reliability metric (e.g., mean_gate)
        score = diagnostics["reliability"]
        
        // 2. Apply Deterministic Logic
        if (score > threshold_high) return {score, PROCEED, diagnostics}
        if (score > threshold_low)  return {score, DOWNWEIGHT, diagnostics}
        return {score, DEFER, diagnostics}
    }
}
```

## 3. Minimal Mathematical Requirements (ResLik Sensor)
To implement the reference sensor (ResLik), you need:
1.  **Reference Mean/Std**: $\mu, \sigma$ (Vectors)
2.  **Normalization**: $z_{norm} = (z - \mu) / \sigma$
3.  **Discrepancy**: $D = |mean(z) - \mu_{ref}| / \sigma_{ref}$
4.  **Gating**: $g = \exp(-\lambda \cdot \max(0, D - \tau))$

## 4. Invariants to Preserve
1.  **No Side Effects**: `update()` must not modify `z`.
2.  **No IO**: `evaluate()` must not access network/disk.
3.  **No Learning**: No gradient updates during inference.
4.  **Separation**: The `ControlSurface` logic must be separate from the `RLCSSensor` math.

```