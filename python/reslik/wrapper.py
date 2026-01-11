from . import _core
from .diagnostics import ResLikDiagnostics, wrap_diagnostics

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
                 gating_lambda: float = 1.0) -> Tuple[np.ndarray, ResLikDiagnostics]:
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
            Tuple[np.ndarray, ResLikDiagnostics]: 
                - Gated output embeddings (n_samples, latent_dim)
                - Structured diagnostics object.
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
            diagnostics_obj = wrap_diagnostics(diagnostics_list[0])
        else:
            # Aggregate diagnostics for batch
            agg_dict = {
                "mean_gate": float(np.mean([d["mean_gate"] for d in diagnostics_list])),
                "max_discrepancy": float(np.max([d["max_discrepancy"] for d in diagnostics_list])),
                "per_sample": diagnostics_list
            }
            diagnostics_obj = wrap_diagnostics(agg_dict)
            
        return outputs, diagnostics_obj