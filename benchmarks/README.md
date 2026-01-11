# ResLik Benchmarks: A Falsification-First Approach

This directory contains scripts designed to stress-test, invalidate, and scope the ResLik method.
Unlike traditional benchmarks that aim to prove superiority, these benchmarks aim to identify:
1. When ResLik fails.
2. Where ResLik adds no value.
3. Whether ResLik's diagnostics correlate with reality.

## Philosophy

> "If a method cannot be falsified, it is not a method."

Our primary metric is **diagnostic utility**, not predictive accuracy.
ResLik is a regularization unit, not a classifier. Therefore, we measure:
- **Stability:** Does it resist noise better than a baseline?
- **Calibration:** Do its "discrepancy scores" actually predict error?
- **Transparency:** Does it fail loudly and informatively under shift?

## Standard Benchmark Template

Every benchmark script in this directory follows this structure:

### 1. Hypothesis
A clear statement of what we expect ResLik to do.
*Example: "ResLik should suppress feature variance when input noise increases."*

### 2. Setup
- **Data:** Synthetic or controlled mock data (no large external datasets).
- **Control:** Baseline model (e.g., identity function, standard scaler).
- **Intervention:** The specific condition being tested (e.g., noise injection, distribution shift).

### 3. Metric
Quantitative measures of success AND failure.
*Example: Cosine similarity drift, Discrepancy-Error correlation.*

### 4. Expected Outcome
What specific result confirms the hypothesis?

### 5. Failure Interpretation
If the benchmark fails (e.g., ResLik performs worse than baseline), what does that mean?
*Example: "If ResLik amplifies noise, the gating mechanism is unstable."*

## Running Benchmarks
Each script is standalone and prints a clear report.
```bash
python benchmarks/stability_shift.py
```
