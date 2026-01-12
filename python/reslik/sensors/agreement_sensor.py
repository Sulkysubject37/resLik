import numpy as np
from typing import Dict, Union, List

class AgreementSensor:
    """
    RLCS-compliant Agreement Sensor (Redundancy Sensor).
    
    This sensor measures the cosine similarity between two independent
    representations z1 and z2 of the same input (e.g., from different encoders
    or augmentations).
    
    It emits scalar signals about agreement, disagreement, and normalized consistency.
    It does NOT fuse or average the representations.
    
    Mathematical Specification:
        A = <z1, z2> / (||z1||*||z2|| + epsilon)
        D = 1 - A
        C = (1 + A) / 2  (Mapped to [0,1])
    """
    
    def __init__(self, epsilon: float = 1e-6):
        """
        Initialize the Agreement Sensor.
        
        Args:
            epsilon (float): Small constant for numerical stability.
        """
        self.epsilon = epsilon
        
    def evaluate(self, z1: Union[np.ndarray, list], z2: Union[np.ndarray, list]) -> Dict[str, float]:
        """
        Evaluate the agreement between two representations.
        
        Args:
            z1 (np.ndarray or list): First representation vector (1D).
            z2 (np.ndarray or list): Second representation vector (1D).
            
        Returns:
            Dict[str, float]: containing:
                - 'agreement': Raw cosine similarity A [-1, 1].
                - 'disagreement': 1 - A [0, 2].
                - 'agreement_consistency': Normalized score C [0, 1].
        """
        z1 = np.array(z1, dtype=np.float32)
        z2 = np.array(z2, dtype=np.float32)
        
        if z1.ndim != 1 or z2.ndim != 1:
            raise ValueError(f"Inputs must be 1D arrays. Got shapes {z1.shape} and {z2.shape}.")
            
        if z1.shape != z2.shape:
             raise ValueError(f"Input shapes must match. Got {z1.shape} and {z2.shape}.")
             
        # Compute Cosine Similarity
        dot_product = np.dot(z1, z2)
        norm1 = np.linalg.norm(z1)
        norm2 = np.linalg.norm(z2)
        
        agreement = dot_product / ((norm1 * norm2) + self.epsilon)
        
        # Clamp agreement to [-1, 1] to handle float precision issues
        agreement = np.clip(agreement, -1.0, 1.0)
        
        disagreement = 1.0 - agreement
        consistency = (1.0 + agreement) / 2.0
        
        return {
            "agreement": float(agreement),
            "disagreement": float(disagreement),
            "agreement_consistency": float(consistency)
        }
