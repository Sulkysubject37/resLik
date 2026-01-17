import sys
import os
import numpy as np

# Add project root for scripts import (append to avoid shadowing installed reslik package)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from reslik.sensors.temporal_consistency import TemporalConsistencySensor
from reslik.sensors.agreement_sensor import AgreementSensor
from scripts.workflows.utils import plot_simulation

def run_simulation():
    print("--- Running Data System Simulation (Concept Drift) ---")
    
    steps = 60
    t_drift_start = 15
    
    # Sensors
    tcs = TemporalConsistencySensor(alpha=2.0)
    agreement = AgreementSensor()
    
    # Data Logs
    log_reslik = []
    log_tcs = []
    log_agreement = []
    
    # State
    z_source_a = np.array([0.5, 0.5])
    z_source_b = np.array([0.5, 0.5])
    
    ref_mean = np.array([0.5, 0.5])
    
    for t in range(steps):
        drift = np.array([0.0, 0.0])
        
        # 1. Simulate Environment
        if t >= t_drift_start:
            # DRIFT: Slow, consistent movement
            # 0.05 per step
            drift = np.array([0.05, 0.05]) * (t - t_drift_start)
            
        current_z_a = z_source_a + drift + np.random.normal(0, 0.01, 2)
        current_z_b = z_source_b + drift + np.random.normal(0, 0.01, 2) # Source B also sees the drift
            
        # 2. Update Sensors
        m_tcs = tcs.update(current_z_a)
        m_agree = agreement.evaluate(current_z_a, current_z_b)
        
        # ResLik (Population check)
        # As drift increases, distance from training mean increases -> ResLik drops
        dist = np.linalg.norm(current_z_a - ref_mean)
        reslik_score = np.exp(-0.5 * dist**2) # Gaussian decay
        
        # 3. Log
        log_reslik.append(reslik_score)
        log_tcs.append(m_tcs['temporal_consistency'])
        log_agreement.append(m_agree['agreement_consistency'])
        
    # 4. Plot
    metrics = {
        'ResLik (Population)': log_reslik,
        'TCS (Temporal)': log_tcs,
        'Agreement (Source A vs B)': log_agreement
    }
    
    plot_simulation(
        range(steps), 
        metrics, 
        "Data System: Concept Drift (Valid Novelty)", 
        "sim_data_drift.png",
        events=[{'t': t_drift_start, 'label': 'Drift Starts'}]
    )

if __name__ == "__main__":
    run_simulation()
