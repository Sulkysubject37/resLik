# How to Self-Validate an RLCS Implementation

You don't need a public benchmark to know if your RLCS implementation works. Use these "Falsification Tests" to verify behavior.

## Test 1: The "Perfect Input" Check
1.  Take a sample directly from your Reference Set (Training Data).
2.  Pass it through the sensor.
3.  **Expected**:
    *   Reliability Score > 0.95.
    *   Control Signal: `PROCEED`.
4.  **Failure**: If score is low, your reference stats are mismatched or normalization is broken.

## Test 2: The "Shock" Check (Temporal)
1.  Pass a vector $z_1$.
2.  Pass a vector $z_2 = z_1 + 10.0$ (Massive jump).
3.  **Expected**:
    *   TCS Drift Score spikes.
    *   TCS Consistency drops to ~0.0.
    *   Control Signal: `ABSTAIN` / `DEFER`.
4.  **Failure**: If consistency remains high, your sensitivity ($\alpha$) is too low or your drift calc is wrong.

## Test 3: The "Noise" Check (Population)
1.  Pass a vector of pure Gaussian noise (mean=0, std=10).
2.  **Expected**:
    *   ResLik Gate Value drops to < 0.1.
    *   Control Signal: `ABSTAIN`.
3.  **Failure**: If the sensor accepts noise, your reference distribution is too broad (high variance).

## Test 4: The "Conflict" Check (Agreement)
1.  Pass $z_A = [1, 0]$.
2.  Pass $z_B = [0, 1]$.
3.  **Expected**:
    *   Agreement Score $\approx 0.0$.
    *   Control Signal: `DEFER` (if logic requires agreement).
4.  **Failure**: If agreement is high, your similarity metric is buggy.
