from abc import ABC, abstractmethod
from typing import Dict, Any
from ..utils import log_execution_time


class BaseTool(ABC):
    """Abstract base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name identifier."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """
        Execute the tool with given arguments.
        
        Returns:
            String result of the tool execution
            
        Raises:
            ToolExecutionError: If execution fails
        """
        pass
    
    def validate_args(self, args: Dict[str, Any]) -> None:
        """
        Validate tool arguments.
        
        Args:
            args: Arguments dictionary
            
        Raises:
            ValidationError: If arguments are invalid
        """
        pass
    
    @log_execution_time
    def run(self, **kwargs) -> str:
        """
        Run the tool with validation and error handling.
        
        Returns:
            Tool execution result
        """
        self.validate_args(kwargs)
        return self.execute(**kwargs)