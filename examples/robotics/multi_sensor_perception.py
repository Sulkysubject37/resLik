import sys
from unittest.mock import MagicMock
sys.modules['reslik._core'] = MagicMock()

import numpy as np
from reslik.sensors.temporal_consistency import TemporalConsistencySensor
from reslik.sensors.agreement_sensor import AgreementSensor
from reslik.diagnostics import ResLikDiagnostics
from reslik.control_surface import ControlAction

def run_robotics_fusion():
    print("--- Multi-Sensor Robotics Perception Demo ---")
    
    # 1. Sensors
    tcs_lidar = TemporalConsistencySensor()
    agreement = AgreementSensor()
    
    # 2. Scenario: "Lidar Blinded by Rain"
    # Lidar embedding becomes noise. Camera embedding remains stable.
    
    # t=0 (Clear)
    z_lidar_t0 = np.array([1.0, 1.0])
    z_cam_t0   = np.array([1.0, 1.0])
    
    # t=1 (Rain)
    z_lidar_t1 = np.array([0.1, 0.9]) # Shifted
    z_cam_t1   = np.array([1.0, 1.0]) # Stable
    
    print("\nEvent: Heavy Rain starts...")
    
    # Update TCS
    tcs_lidar.update(z_lidar_t0)
    metrics_tcs = tcs_lidar.update(z_lidar_t1)
    
    # Update Agreement
    metrics_agree = agreement.evaluate(z_lidar_t1, z_cam_t1)
    
    # Mock ResLik (Lidar looks OOD)
    reslik_score = 0.4 
    
    print(f"[ResLik] Lidar Reliability: {reslik_score:.2f} (Low)")
    print(f"[TCS]    Lidar Stability:   {metrics_tcs['temporal_consistency']:.2f} (Modest Drift)")
    print(f"[Agree]  Lidar vs Camera:   {metrics_agree['agreement_consistency']:.2f} (Conflict)")
    
    # 3. Control Decision
    # If ResLik is low AND Agreement is low, we trust the OTHER sensor (Camera).
    
    if reslik_score < 0.5 and metrics_agree['agreement_consistency'] < 0.6:
        print("\n[Control] Action: SWITCH_MODALITY")
        print(">> Logic: Lidar is OOD and conflicts with Camera. Switching to Camera-Dominant Navigation.")
    else:
        print("\n[Control] Action: FUSE_NORMALLY")

if __name__ == "__main__":
    run_robotics_fusion()
