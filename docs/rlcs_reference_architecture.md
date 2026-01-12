# RLCS Reference Architecture

This document visualizes the standard data and control flow in an RLCS-compliant system.

## Layered Architecture

```text
+---------------------------------------------------------------+
|                      Application Layer                        |
|  (User Interface, Business Logic, Mission Planning)           |
+---------------------------------------------------------------+
            ^                       |
            | Decisions             | Context / Goals
            |                       v
+-----------|-----------------------|---------------------------+
|           |       External Controller (ACTING)                |
|           |  [Policy Engine / State Machine / Fusion]         |
+-----------|-----------------------|---------------------------+
            ^                       ^
            | Control Signal        |
            | (Recommendation)      |
+-----------|-----------------------|---------------------------+
|           |       Control Surface (SIGNALING)                 |
|           |  [Thresholds / Mapping Logic / Stateless]         |
+-----------|-----------------------|---------------------------+
|           | Diagnostics           |
            | (Raw Metrics)         |
+-----------|-----------------------|---------------------------+
|           |     RLCS Sensor Array (SENSING)                   |
|           |  [ResLik / TCS / Composable Units]                |
+-----------|-----------------------|---------------------------+
            ^                       ^
            | Latent Z              |
            |                       |
+-----------|-----------------------|---------------------------+
|           |        Encoder / Model (LEARNING)                 |
|           |  [Deep Net / Feature Extractor / Transformer]     |
+-----------|-----------------------|---------------------------+
            ^
            |
      Raw Input Data
```

## Layer Responsibilities

1.  **Encoder (Learning)**
    *   **Input**: Raw Data.
    *   **Output**: Latent Representation ($z$).
    *   **Responsibility**: Extract semantic features. *Ignorant of reliability.*

2.  **RLCS Sensor Array (Sensing)**
    *   **Input**: Latent Representation ($z$).
    *   **Output**: Composite Diagnostics ($d$) + Gated Representation ($z'$).
    *   **Responsibility**: Measure statistical consistency (Population & Temporal). *Ignorant of system goals.*

3.  **Control Surface (Signaling)**
    *   **Input**: Diagnostics ($d$).
