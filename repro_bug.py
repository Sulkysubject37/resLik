import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class DiagnosticReport:
    mean_gate_value: float
    max_discrepancy: float

class MockCoreUnit:
    def __init__(self, d, h):
        pass
    def set_reference_stats(self, m, s): pass
    def set_lambda(self, l): pass
    def set_tau(self, t): pass
    def forward(self, x): return np.zeros(10)
    def get_diagnostics(self):
        return DiagnosticReport(0.5, 0.1)

class ResLikUnitMock:
    def __init__(self, input_dim, latent_dim):
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self._cpp_unit = MockCoreUnit(input_dim, latent_dim)

    def __call__(self, z_in):
        # Input Validation
        z_in = np.asarray(z_in, dtype=np.float32)
        
        if z_in.size == 0:
            raise ValueError("Input array is empty.")

        if z_in.ndim == 1:
            is_batch = False
            z_in = z_in[np.newaxis, :]
        elif z_in.ndim == 2:
            is_batch = True
        else:
            raise ValueError(f"Input must be 1D or 2D array, got {z_in.ndim}D.")
            
        print(f"DEBUG: z_in.shape={z_in.shape}, is_batch={is_batch}")
        
        outputs = []
        diagnostics_list = []
        
        for i in range(z_in.shape[0]):
            sample = z_in[i]
            # Mock C++ call
            out_vec = self._cpp_unit.forward(sample)
            diag = self._cpp_unit.get_diagnostics()
            
            outputs.append(out_vec)
            diagnostics_list.append({
                "mean_gate": diag.mean_gate_value,
                "max_discrepancy": diag.max_discrepancy
            })
            
        print(f"DEBUG: diagnostics_list len={len(diagnostics_list)}")
        
        outputs = np.array(outputs, dtype=np.float32)
        
        if not is_batch:
            outputs = outputs[0]
            # diagnostics_obj = wrap_diagnostics(diagnostics_list[0])
            print("Single mode")
        else:
            print("Batch mode")
            # Aggregate diagnostics for batch
            agg_dict = {
                "mean_gate": float(np.mean([d["mean_gate"] for d in diagnostics_list])),
                "max_discrepancy": float(np.max([d["max_discrepancy"] for d in diagnostics_list])),
                "per_sample": diagnostics_list
            }
            print("Aggregated")
            
        return outputs

def run_test():
    unit = ResLikUnitMock(20, 10)
    data = np.random.randn(5, 20).astype(np.float32)
    unit(data)
    print("Test passed")

if __name__ == "__main__":
    run_test()
