import numpy as np
from typing import Tuple, Dict, Any, Optional
from . import _core

class ResLikUnit:
    """
    ResLik: Residual Likelihood-Gated Representation Unit.
    
    This unit applies a soft, learned gate to feature embeddings based on their
    statistical consistency with a reference distribution (e.g., healthy controls).
    
    It wraps the optimized C++ implementation.
    """
    
    def __init__(self, input_dim: int, latent_dim: int = 64):
        """
        Initialize the ResLik Unit.
        
        Args:
            input_dim (int): Dimension of the input feature embeddings.
            latent_dim (int): Dimension of the internal projection layer.
        """
        if input_dim <= 0 or latent_dim <= 0:
            raise ValueError("Dimensions must be positive integers.")
            
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self._cpp_unit = _core.ResLikUnit(input_dim, latent_dim)
        
    def __call__(self, 
                 z_in: np.ndarray, 
                 ref_mean: float = 0.0, 
                 ref_std: float = 1.0, 
                 gating_lambda: float = 1.0) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Apply ResLik gating to the input embeddings.
        
        Args:
            z_in (np.ndarray): Input feature matrix of shape (n_samples, input_dim) 
                               or vector of shape (input_dim,).
            ref_mean (float): Reference mean for the current feature set. 
                              (Currently shared scalar for Phase 2).
            ref_std (float): Reference standard deviation. Must be > 0.
            gating_lambda (float): Sensitivity of the gating mechanism. Higher values
                                   mean stricter filtering of outliers.
                                   
        Returns:
            Tuple[np.ndarray, Dict[str, Any]]: 
                - Gated output embeddings (same shape as input, but projected dim if fully implemented, 
                  here currently C++ returns same dim 'a' * gate, actually it returns latent_dim sized vector from project()?)
                  Wait, C++ logic: f (latent_dim), s (scalar), a = f * s (latent_dim). 
                  So output is (latent_dim).
                - Diagnostics dictionary containing discrepancy scores and gate values.
        """
        # Input Validation
        z_in = np.asarray(z_in, dtype=np.float32)
        
        if z_in.ndim == 1:
            is_batch = False
            z_in = z_in[np.newaxis, :]
        elif z_in.ndim == 2:
            is_batch = True
        else:
            raise ValueError(f"Input must be 1D or 2D array, got {z_in.ndim}D.")
            
        if z_in.shape[1] != self.input_dim:
            raise ValueError(f"Input feature dimension {z_in.shape[1]} does not match initialized dimension {self.input_dim}.")
            
        if not np.all(np.isfinite(z_in)):
            raise ValueError("Input contains NaNs or Infinities.")
            
        if ref_std <= 0:
            raise ValueError(f"Reference standard deviation must be positive, got {ref_std}.")

        # Set Unit State
        self._cpp_unit.set_reference_stats(ref_mean, ref_std)
        self._cpp_unit.set_lambda(gating_lambda)
        
        # Process Batch (Looping in Python for Phase 2/3 simplicity, C++ handles single vector)
        # Future optimization: Move batch loop to C++
        outputs = []
        diagnostics_list = []
        
        for i in range(z_in.shape[0]):
            sample = z_in[i]
            out_vec = self._cpp_unit.forward(sample)
            diag = self._cpp_unit.get_diagnostics()
            
            outputs.append(out_vec)
            diagnostics_list.append({
                "mean_gate": diag.mean_gate_value,
                "max_discrepancy": diag.max_discrepancy
            })
            
        outputs = np.array(outputs, dtype=np.float32)
        
        if not is_batch:
            outputs = outputs[0]
            diagnostics_agg = diagnostics_list[0]
        else:
            # Aggregate diagnostics for batch
            diagnostics_agg = {
                "mean_gate": np.mean([d["mean_gate"] for d in diagnostics_list]),
                "max_discrepancy": np.max([d["max_discrepancy"] for d in diagnostics_list]),
                "per_sample": diagnostics_list
            }
            
        return outputs, diagnostics_agg