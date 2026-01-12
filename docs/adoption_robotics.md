# RLCS Adoption Template: Robotics Perception

**Target System**: Sensor Fusion Stacks (e.g., Lidar+Camera fusion, SLAM, Obstacle Avoidance).

## 1. Where RLCS Fits
Attach an RLCS Sensor to the feature extraction layer of each modality *before* the fusion center.

```text
[Lidar Raw] -> [Lidar Encoder] -> [z_lidar] -> [RLCS Sensor A] --(signal A)--> [Fusion Controller]
                                                                                      ^
[Camera Raw] -> [Camera Encoder] -> [z_cam] -> [RLCS Sensor B] --(signal B)-----------|
```

## 2. Signals Consumed
*   **Fusion Controller** consumes `ControlSignal` (reliability scores).
    *   **Weighting**: Use `reliability_score` to dynamically adjust the Kalman Filter variance or fusion attention weights.
    *   **Mode Switching**: If Lidar is `ABSTAIN` (e.g., due to heavy rain causing OOD reflections), switch to "Radar-Only" navigation mode.

## 3. External Decisions (What YOU define)
*   **Safety Constraints**: At what reliability threshold do you trigger an E-Stop?
*   **Degradation Policy**: How fast does the robot move in "degraded" mode?

## 4. Anti-Patterns (What NOT to do)
*   Do not let the RLCS Sensor trigger the E-Stop directly. The sensor does not know if the robot is in a busy intersection or a parking lot. Only the Controller knows the context.
