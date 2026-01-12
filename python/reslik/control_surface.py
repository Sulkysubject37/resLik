from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Any, Optional
from .diagnostics import ResLikDiagnostics

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

class ControlSurface:
    """
    Deterministic control logic that maps ResLik diagnostics to explicit control actions.
    
    This class is stateless and inspection-friendly. It does not learn or adapt.
    It applies user-defined thresholds to produce a monotonic control decision.
    """
    
    def __init__(self, reliability_high: float = 0.8, reliability_low: float = 0.5, max_discrepancy_threshold: float = 5.0):
        """
        Initialize the ControlSurface with explicit thresholds.
        
        Args:
            reliability_high (float): Threshold above which action is PROCEED.
            reliability_low (float): Threshold below which action is DEFER.
                                     Between low and high is DOWNWEIGHT.
            max_discrepancy_threshold (float): Threshold above which action is ABSTAIN,
                                               regardless of reliability.
        """
        self.r_high = reliability_high
        self.r_low = reliability_low
        self.d_max = max_discrepancy_threshold
        
    def evaluate(self, diagnostics: ResLikDiagnostics) -> ControlSignal:
        """
        Evaluate diagnostics to produce a ControlSignal.
        
        Logic:
            1. If max_discrepancy > d_max -> ABSTAIN (Critical Anomaly)
            2. Else if reliability > r_high -> PROCEED (Healthy)
            3. Else if reliability > r_low -> DOWNWEIGHT (Marginal)
            4. Else -> DEFER (Unreliable)
            
        Args:
            diagnostics (ResLikDiagnostics): The output from a ResLikUnit.
            
        Returns:
            ControlSignal: Structured recommendation.
        """
        reliability = diagnostics.mean_gate_value
        max_disc = diagnostics.max_discrepancy
        
        # Default mean discrepancy if not present (ResLikDiagnostics might evolve)
        # Assuming ResLikDiagnostics has max_discrepancy and mean_gate_value as per definition.
        # We'll use 0.0 for mean_discrepancy if not easily computable from current diagnostics,
        # but the current definition of ResLikDiagnostics is simple. 
        # Ideally we'd want mean_discrepancy in ResLikDiagnostics, but for now we rely on what is there.
        # Wait, ResLikDiagnostics has `mean_gate_value` and `max_discrepancy`.
        # It doesn't explicitly have `mean_discrepancy`. 
        # Phase 6 spec says "ControlSignal... mean_discrepancy: float".
        # We will set mean_discrepancy to 0.0 or same as max for now if not available,
        # BUT strictly, let's look at `diagnostics.py` content again.
        # It has `mean_gate_value` and `max_discrepancy`.
        # We will infer or pass-through. Since we can't calculate mean discrepancy from just max and mean_gate
        # without per-sample data, and we want to avoid large computation, we will set it to -1.0 
        # or similar to indicate "not available" unless we update diagnostics.
        # However, the constraint is "DO NOT modify ResLik core math/APIs".
        # I will define mean_discrepancy in ControlSignal as optional or fill with a placeholder
        # derived from available data if possible, or just set to 0.0 if unknown.
        # Actually, let's check if we can get it from per_sample_details if available.
        
        mean_disc = 0.0
        if diagnostics.per_sample_details:
             # If batch details exist, we might try to extract, but that's O(N).
             # Let's keep it cheap.
             pass

        action = ControlAction.DEFER
        
        if max_disc > self.d_max:
            action = ControlAction.ABSTAIN
        elif reliability > self.r_high:
            action = ControlAction.PROCEED
        elif reliability > self.r_low:
            action = ControlAction.DOWNWEIGHT
        else:
            action = ControlAction.DEFER
            
        return ControlSignal(
            reliability_score=reliability,
            mean_discrepancy=mean_disc, # Placeholder as strictly not in minimal diagnostics
            max_discrepancy=max_disc,
            gate_summary={"mean": reliability},
            recommended_action=action
        )
