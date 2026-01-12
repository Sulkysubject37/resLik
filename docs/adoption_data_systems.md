# RLCS Adoption Template: Data Systems

**Target System**: High-Throughput Ingestion, ETL Pipelines, Feature Stores.

## 1. Where RLCS Fits
Integrate RLCS as a "Quality Gate" stage within the ingestion worker or stream processor.

```text
[Data Stream] -> [Feature Extractor] -> [z_vector] -> [RLCS Sensor] -> [Feature Store]
                                                            |
                                                            v
                                                    [Control Surface] -> [Signal] -> [Ingestion Manager]
```

## 2. Signals Consumed
*   **Ingestion Manager** consumes `ControlAction`.
    *   `PROCEED`: Write vector to the Feature Store.
    *   `DOWNWEIGHT`: Write to Feature Store with a "Low Quality" tag/flag.
    *   `ABSTAIN`: Drop the record and log to a "Dead Letter Queue" for debugging.

## 3. External Decisions (What YOU define)
*   **Retention Policy**: How long to keep "Low Quality" data?
*   **Alerting**: When to wake up a data engineer (e.g., if >10% of batch is `ABSTAIN`)?

## 4. Anti-Patterns (What NOT to do)
*   Do not auto-retrain the model based on RLCS flags without human verification. A spike in `ABSTAIN` might mean the world changed (drift) or the sensor broke.
