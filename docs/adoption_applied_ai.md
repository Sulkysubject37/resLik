# RLCS Adoption Template: Applied AI Pipelines

**Target System**: Multi-stage Inference Pipelines (e.g., RAG, chained models, cascading classifiers).

## 1. Where RLCS Fits
Insert the RLCS Sensor immediately after the primary embedding stage, before the vector is passed to downstream tasks (retrieval, classification).

```text
[Input Text/Image] -> [Encoder Model] -> [Vector z] -> [RLCS Sensor] -> [Gated z'] -> [Downstream Task]
                                                            |
                                                            v
                                                    [Control Surface] -> [Signal] -> [Pipeline Orchestrator]
```

## 2. Signals Consumed
*   **Pipeline Orchestrator** consumes `ControlAction`.
    *   `PROCEED`: Continue with expensive downstream inference.
    *   `DEFER`: Route to a lightweight fallback model or cache lookup.
    *   `ABSTAIN`: Return a "Low Confidence" error to the user immediately.

## 3. External Decisions (What YOU define)
*   **Routing Logic**: Which fallback model to use?
*   **User Messaging**: What to tell the user when abstaining?
*   **Latency Budget**: How much delay is acceptable for the check?

## 4. Anti-Patterns (What NOT to do)
*   Do not use RLCS to "fix" a hallucinating LLM. If the embedding is coherent but factually wrong, RLCS (consistency sensor) might not catch it. It catches *statistical* anomalies.
