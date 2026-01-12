from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Any

class ControlAction(Enum):
    """
    Recommended actions for downstream systems based on ResLik signals.
    
    Values:
        PROCEED: The representation is reliable and consistent with the reference.
        DOWNWEIGHT: The representation has minor inconsistencies; reduce its influence.
        DEFER: The representation is unreliable; defer to a fallback system or human.
        ABSTAIN: The representation is critically anomalous; do not use it.
    """
    PROCEED = auto()
    DOWNWEIGHT = auto()
    DEFER = auto()
    ABSTAIN = auto()

@dataclass
class ControlSignal:
    """
    Formal container for control recommendations derived from ResLik diagnostics.
    
    Attributes:
        reliability_score (float): A scalar [0, 1] indicating overall representation health.
                                   Higher is better. Typically derived from mean gate value.
        mean_discrepancy (float): Average statistical deviation from the reference.
        max_discrepancy (float): Maximum statistical deviation observed in the input.
        gate_summary (Dict[str, float]): Summary statistics of the gating mask (e.g., mean, min).
        recommended_action (ControlAction): The explicit action suggested by the control surface.
    """
    reliability_score: float
    mean_discrepancy: float
    max_discrepancy: float
    gate_summary: Dict[str, float]
    recommended_action: ControlAction
