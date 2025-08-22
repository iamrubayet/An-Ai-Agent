class AgentError(Exception):
    """Base exception for agent errors."""
    pass


class ToolExecutionError(AgentError):
    """Raised when a tool fails to execute."""
    pass


class PlanningError(AgentError):
    """Raised when planning fails."""
    pass


class ValidationError(AgentError):
    """Raised when input validation fails."""
    pass