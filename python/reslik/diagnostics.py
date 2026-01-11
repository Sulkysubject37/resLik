from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional
import numpy as np

@dataclass
class ResLikDiagnostics:
    """
    Structured container for ResLik diagnostic outputs.
    """
    mean_gate_value: float
    max_discrepancy: float
    per_sample_details: Optional[List[Dict[str, float]]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert diagnostics to a standard dictionary."""
        return asdict(self)
    
    def summary(self) -> str:
        """Return a human-readable summary string."""
        return (
            f"ResLik Diagnostics:\n"
            f"  Mean Gate Value: {self.mean_gate_value:.4f} (Lower = More Suppression)\n"
            f"  Max Discrepancy: {self.max_discrepancy:.4f} (Higher = More Outlier-ish)"
        )

def wrap_diagnostics(raw_dict: Dict[str, Any]) -> ResLikDiagnostics:
    """
    Factory function to create a ResLikDiagnostics object from the wrapper output.
    """
    return ResLikDiagnostics(
        mean_gate_value=raw_dict.get("mean_gate", 0.0),
        max_discrepancy=raw_dict.get("max_discrepancy", 0.0),
        per_sample_details=raw_dict.get("per_sample")
    )