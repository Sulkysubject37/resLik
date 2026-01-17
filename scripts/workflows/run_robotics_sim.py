import sys
import os
import numpy as np

# Add python source directory to sys.path (prepend to avoid conflict with root reslik/ folder)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../python')))
# Add project root for scripts import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Mock the C++ core
from unittest.mock import MagicMock
sys.modules['reslik._core'] = MagicMock()

from reslik.sensors.temporal_consistency import TemporalConsistencySensor
from reslik.sensors.agreement_sensor import AgreementSensor
from scripts.workflows.utils import plot_simulation

def run_simulation():
    print("--- Running Robotics Simulation (Lidar Rain Noise) ---")
    
    steps = 60
    t_rain_start = 20
    
    # Sensors
    tcs = TemporalConsistencySensor(alpha=1.0)
    agreement = AgreementSensor()
    
    # Data Logs
    log_reslik = []
    log_tcs = []
    log_agreement = []
    
    # State
    z_lidar = np.array([1.0, 1.0]) # Initial state (Normal)
    z_cam   = np.array([1.0, 1.0]) # Initial state (Normal)
    
    # Mock Reference Mean for ResLik
    ref_mean = np.array([1.0, 1.0])
    
    for t in range(steps):
        # 1. Simulate Environment
        if t >= t_rain_start:
            # RAIN: Lidar signal gets biased and noisy
            noise = np.random.normal(0, 0.1, 2)
            bias = np.array([-0.5, 0.5]) * ((t - t_rain_start) / 10.0) # Gradual drift away
            current_z_lidar = z_lidar + bias + noise
            # Camera stays relatively true
            current_z_cam = z_cam + np.random.normal(0, 0.05, 2)
        else:
            # CLEAR: Small noise
            current_z_lidar = z_lidar + np.random.normal(0, 0.05, 2)
            current_z_cam = z_cam + np.random.normal(0, 0.05, 2)
            
        # 2. Update Sensors
        
        # TCS (on Lidar)
        m_tcs = tcs.update(current_z_lidar)
        
        # Agreement (Lidar vs Camera)
        m_agree = agreement.evaluate(current_z_lidar, current_z_cam)
        
        # ResLik (Mock Population Check on Lidar)
        # Distance from "Normal" mean
        dist = np.linalg.norm(current_z_lidar - ref_mean)
        # Simple Gaussian gate
        reslik_score = np.exp(-1.0 * dist)
        
        # 3. Log
        log_reslik.append(reslik_score)
        log_tcs.append(m_tcs['temporal_consistency'])
        log_agreement.append(m_agree['agreement_consistency'])
        
    # 4. Plot
    metrics = {
        'ResLik (Population)': log_reslik,
        'TCS (Temporal)': log_tcs,
        'Agreement (Cross-Modal)': log_agreement
    }
    
    plot_simulation(
        range(steps), 
        metrics, 
        "Robotics Sensor Fusion: Lidar Rain Event", 
        "sim_robotics_rain.png",
        events=[{'t': t_rain_start, 'label': 'Rain Starts'}]
    )

if __name__ == "__main__":
    run_simulation()
