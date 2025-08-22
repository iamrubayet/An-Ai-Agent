from typing import Dict, Any, Optional
from pydantic import BaseModel, validator
from enum import Enum


class ToolName(str, Enum):
    """Enumeration of available tools."""
    CALCULATOR = "calculator"
    WEATHER = "weather"
    KNOWLEDGE_BASE = "kb"
    UNIT_CONVERTER = "unitconv"
    TRANSLATOR = "translator"  # New tool


class ToolPlan(BaseModel):
    """Schema for tool execution plan."""
    tool: ToolName
    args: Dict[str, Any]
    
    @validator('args')
    def validate_args(cls, v, values):
        """Validate arguments based on tool type."""
        if 'tool' not in values:
            return v
            
        tool = values['tool']
        required_args = {
            ToolName.CALCULATOR: ['expr'],
            ToolName.WEATHER: ['city'],
            ToolName.KNOWLEDGE_BASE: ['query'],
            ToolName.UNIT_CONVERTER: ['query'],
            ToolName.TRANSLATOR: ['text', 'from_lang', 'to_lang']
        }
        
        if tool in required_args:
            for arg in required_args[tool]:
                if arg not in v:
                    raise ValueError(f"Tool '{tool}' requires argument '{arg}'")
        
        return v


class AgentResponse(BaseModel):
    """Schema for agent response."""
    result: str
    tool_used: Optional[ToolName] = None
    success: bool = True
    error: Optional[str] = None