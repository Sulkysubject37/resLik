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
    print("--- Running AI Pipeline Simulation (Transient Shock) ---")
    
    steps = 50
    t_shock = 25
    
    # Sensors
    tcs = TemporalConsistencySensor(alpha=3.0) # High sensitivity
    agreement = AgreementSensor()
    
    # Data Logs
    log_reslik = []
    log_tcs = []
    log_agreement = []
    
    # State
    z_primary = np.array([1.0, 0.0])
    z_backup  = np.array([0.9, 0.1])
    
    for t in range(steps):
        # 1. Simulate Environment
        if t == t_shock:
            # SHOCK: Massive spike in Primary
            current_z_primary = np.array([5.0, 5.0]) 
            # Backup sensor misses the glitch (or filters it)
            current_z_backup = z_backup + np.random.normal(0, 0.02, 2)
            
            # Mock ResLik Failure:
            # Assume the model hallucinates confidence for this specific glitch
            reslik_score = 0.95 
        else:
            # Normal
            current_z_primary = z_primary + np.random.normal(0, 0.05, 2)
            current_z_backup = z_backup + np.random.normal(0, 0.05, 2)
            reslik_score = 0.9 + np.random.normal(0, 0.02)

        # 2. Update Sensors
        m_tcs = tcs.update(current_z_primary)
        m_agree = agreement.evaluate(current_z_primary, current_z_backup)
        
        # 3. Log
        log_reslik.append(reslik_score)
        log_tcs.append(m_tcs['temporal_consistency'])
        log_agreement.append(m_agree['agreement_consistency'])
        
    # 4. Plot
    metrics = {
        'ResLik (Population)': log_reslik,
        'TCS (Temporal)': log_tcs,
        'Agreement (Cross-Model)': log_agreement
    }
    
    plot_simulation(
        range(steps), 
        metrics, 
        "AI Pipeline: Transient Shock (ResLik False Positive)", 
        "sim_ai_shock.png",
        events=[{'t': t_shock, 'label': 'Shock'}]
    )

if __name__ == "__main__":
    run_simulation()
