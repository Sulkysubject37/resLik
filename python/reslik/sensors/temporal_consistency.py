import numpy as np
from typing import Dict, Optional, Union

class TemporalConsistencySensor:
    """
    RLCS-compliant Temporal Consistency Sensor (TCS).
    
    This sensor measures whether representations evolve coherently over time by
    comparing the current representation z_t with the immediately previous
    representation z_{t-1}.
    
    It maintains minimal state (only z_{t-1}) and computes a normalized temporal
    drift score and a mapped consistency score.
    
    Mathematical Specification:
        D_t = ||z_t - z_{t-1}||_2 / (||z_{t-1}||_2 + epsilon)
        T_t = exp(-alpha * D_t)
        
    where alpha > 0 controls sensitivity.
    """
    
    def __init__(self, alpha: float = 1.0, epsilon: float = 1e-6):
        """
        Initialize the Temporal Consistency Sensor.
        
        Args:
            alpha (float): Sensitivity parameter > 0. Controls how aggressively drift is penalized.
                           Higher alpha -> steeper drop in consistency score for same drift.
            epsilon (float): Small constant for numerical stability during normalization.
        """
        if alpha <= 0:
            raise ValueError("Alpha must be positive.")
        
        self.alpha = alpha
        self.epsilon = epsilon
        self._prev_z: Optional[np.ndarray] = None
        
    def update(self, z_t: Union[np.ndarray, list]) -> Dict[str, float]:
        """
        Observe the current representation z_t and compute temporal consistency metrics.
        
        Args:
            z_t (np.ndarray or list): Current representation vector at time t.
                                      Must be 1D array-like.
            
        Returns:
            Dict[str, float]: containing:
                - 'temporal_drift': The normalized drift score D_t.
                - 'temporal_consistency': The mapped consistency score T_t [0, 1].
                
        Note:
            For the first update (t=0), drift is 0.0 and consistency is 1.0.
        """
        z_t = np.array(z_t, dtype=np.float32)
        
        if z_t.ndim != 1:
            raise ValueError(f"Input z_t must be 1D, got shape {z_t.shape}")
            
        if self._prev_z is None:
            # First time step: no history to compare against.
            # Assume perfect consistency.
            self._prev_z = z_t.copy()
            return {
                "temporal_drift": 0.0,
                "temporal_consistency": 1.0
            }
            
        # 1. Compute Raw Temporal Deviation
        # delta_t = ||z_t - z_{t-1}||_2
        diff = z_t - self._prev_z
        delta_t = np.linalg.norm(diff)
        
        # 2. Compute Normalized Temporal Drift Score
        # D_t = delta_t / (||z_{t-1}||_2 + epsilon)
        norm_prev = np.linalg.norm(self._prev_z)
        drift_score = delta_t / (norm_prev + self.epsilon)
        
        # 3. Compute Temporal Consistency Score
        # T_t = exp(-alpha * D_t)
        consistency_score = np.exp(-self.alpha * drift_score)
        
        # Update state for next step
        self._prev_z = z_t.copy()
        
        return {
            "temporal_drift": float(drift_score),
            "temporal_consistency": float(consistency_score)
        }
    
    def reset(self):
        """Clear the sensor state (forget z_{t-1})."""
        self._prev_z = None
