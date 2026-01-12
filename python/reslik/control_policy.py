from typing import Any, Dict, Protocol
from .diagnostics import ResLikDiagnostics

class ControlPolicy(Protocol):
    """
    Interface definition for external control logic consuming ResLik signals.
    
    A ControlPolicy receives diagnostics from a ResLikUnit and returns a 
    decision regarding the execution flow of the parent system.
    
    IMPORTANT: ResLik itself does not implement these policies. This interface
    serves as a template for downstream system integration.
    """
    
    def decide(self, diagnostics: ResLikDiagnostics, context: Dict[str, Any] = None) -> Any:
        """
        Evaluate ResLik diagnostics to produce an execution decision.
        
        Args:
            diagnostics (ResLikDiagnostics): The signals emitted by ResLik.
            context (Dict[str, Any], optional): External system state required for 
                                                contextual decision making.
        
        Returns:
            Any: A system-defined decision (e.g., Boolean flag, routing key, 
                 or numerical scale factor).
        """
        ...

class ExecutionDecision:
    """
    Template for structured execution decisions.
    
    This class can be used to wrap the output of a ControlPolicy, 
    separating the reliability signal from the resulting action.
    """
    def __init__(self, action_id: str, confidence: float, metadata: Dict[str, Any] = None):
        self.action_id = action_id
        self.confidence = confidence
        self.metadata = metadata or {}
