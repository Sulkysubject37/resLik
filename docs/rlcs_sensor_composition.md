# RLCS Sensor Composition Rules

This document defines the architectural principles for composing multiple RLCS sensors (e.g., ResLik + TCS + Agreement) into a unified reliability system.

## 1. Composition Principle
**"RLCS sensors are parallel observers, not competing predictors."**

When multiple sensors are active, they run in parallel. They do not feed into each other, and they do not attempt to predict the output of their peers. Each sensor provides a distinct, orthogonal slice of the reliability state space.

## 2. The Non-Arbitration Rule
*   **Rule**: Sensors do not overrule each other.
*   **Implication**: If ResLik says "Safe" and TCS says "Unsafe," the system state is "Ambiguous/Unsafe." ResLik does not "vote down" TCS.
*   **Control Logic**: The Control Surface consumes the union of all signals. It typically adopts a "conservative logical OR" for safety warnings (i.e., if *any* sensor flags danger, the signal reflects danger).

## 3. The Independence Invariant
Each sensor in an RLCS array must satisfy:
1.  **Distinct Reference**: It must measure consistency against a unique reference frame (Population vs. History vs. Peer).
2.  **Isolated Interpretability**: The signal from Sensor A must be meaningful even if Sensor B is removed. A sensor cannot output a "correction factor" for another sensor.

## 4. Valid Composition Patterns

### Pattern A: The Safety Triangulation (ResLik + TCS + Agreement)
*   **ResLik**: "Is this input weird compared to training data?" (OOD)
*   **TCS**: "Did this input just jump out of nowhere?" (Shock)
*   **Agreement**: "Do my eyes agree with my ears?" (Conflict)
*   **Result**: A comprehensive 360-degree view of reliability.

### Pattern B: The Glitch Filter (ResLik + TCS)
*   **Use Case**: Video streams.
*   **Logic**: ResLik filters semantic nonsense; TCS filters transmission artifacts.

### Pattern C: The Redundancy Check (ResLik + Agreement)
*   **Use Case**: Sensor fusion stacks.
*   **Logic**: ResLik validates the primary sensor; Agreement validates it against the secondary sensor.

## 5. Invalid Patterns (Anti-Patterns)

### Anti-Pattern 1: Majority Voting
*   **Bad**: "2 out of 3 sensors say Safe, so we proceed."
*   **Why**: Sensors measure *different things*. If TCS screams "Shock," it doesn't matter that ResLik thinks the frame looks "Normal." The shock is real.

### Anti-Pattern 2: Weighted Averaging
*   **Bad**: `FinalScore = 0.5 * ResLik + 0.3 * TCS + 0.2 * Agreement`
*   **Why**: This hides the failure mode. A low TCS score (shock) gets drowned out by a high ResLik score (valid content), masking the danger.

### Anti-Pattern 3: Feature Fusion
*   **Bad**: Using sensor scores to mix latent vectors: `z_new = z1 * score1 + z2 * score2`.
*   **Why**: This turns the sensor into a controller/modifier. RLCS sensors only *signal*; they do not *construct* data.
