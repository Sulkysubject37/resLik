# Position on Differentiability

The question of whether an RLCS sensor *should* be differentiable is nuanced. This document clarifies the project's stance to prevent confusion between "control surfaces" and "regularizers."

## 1. Why ResLik v1.0 is Forward-Only
ResLik v1.0 explicitly omits backpropagation support for specific reasons:
1.  **Safety & Stability**: A non-differentiable component acts as a "firewall." It prevents the Encoder from "gaming" the reliability metric during training (i.e., learning to fool the sensor rather than improving the representation).
2.  **Simplicity**: It enforces the usage pattern of "Encoder first, Sensor second."
3.  **Portability**: A pure numerical implementation (C++) is easier to deploy in constrained environments (embedded, mobile) than a full autograd graph.

## 2. When Differentiability is Useful
Differentiability is **optional** but valid within RLCS if the goal shifts from *runtime control* to *model training*:
*   **Representation Regularization**: If the sensor provides gradients, the `discrepancy` score can be added to the training loss function ($\mathcal{L}_{total} = \mathcal{L}_{task} + \lambda \mathcal{L}_{discrepancy}$). This encourages the Encoder to produce "reliable-by-design" embeddings.

## 3. The RLCS Stance
**RLCS does not require gradients.**

*   The core value of RLCS is **runtime reliability sensing**, which is an inference-time activity.
*   Differentiability is an *extension* for training time, not a requirement for the paradigm.
*   **Warning**: Collapsing sensing into optimization (training the sensor and encoder jointly without care) risks "Goodhart's Law"—when a measure becomes a target, it ceases to be a good measure.

## 4. Conclusion
While future sensors may include `backward()` methods, the RLCS paradigm is defined by its ability to *inform control*, not its ability to propagate gradients.
