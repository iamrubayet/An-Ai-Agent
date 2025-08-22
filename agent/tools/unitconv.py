import re
from typing import Dict, Any, Callable, Union
from .base import BaseTool
from ..exceptions import ToolExecutionError, ValidationError


class UnitConverterTool(BaseTool):
    """Tool for converting between different units."""
    
    def __init__(self):
        self._conversions = self._init_conversions()
    
    @property
    def name(self) -> str:
        return "unitconv"
    
    def _init_conversions(self) -> Dict[tuple, Union[float, Callable]]:
        """Initialize conversion factors and functions."""
        return {
            # Currency conversions (mock rates)
            ("usd", "eur"): 0.9,
            ("eur", "usd"): 1.1,
            ("usd", "gbp"): 0.8,
            ("gbp", "usd"): 1.25,
            ("eur", "gbp"): 0.85,
            ("gbp", "eur"): 1.18,
            
            # Temperature conversions
            ("c", "f"): lambda x: (x * 9/5) + 32,
            ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
            ("f", "c"): lambda x: (x - 32) * 5/9,
            ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
            
            # Length conversions
            ("m", "ft"): 3.28084,
            ("ft", "m"): 0.3048,
            ("km", "mi"): 0.621371,
            ("mi", "km"): 1.60934,
            
            # Weight conversions
            ("kg", "lb"): 2.20462,
            ("lb", "kg"): 0.453592,
        }
    
    def validate_args(self, args: Dict[str, Any]) -> None:
        """Validate unit converter arguments."""
        if "query" not in args:
            raise ValidationError("Unit converter requires 'query' argument")
        
        if not isinstance(args["query"], str):
            raise ValidationError("Query must be a string")
    
    def execute(self, query: str, **kwargs) -> str:
        """
        Convert between units based on query.
        
        Args:
            query: Conversion query like "Convert 10 USD to EUR"
            
        Returns:
            Converted value as string
        """
        try:
            # Parse the conversion query
            value, from_unit, to_unit = self._parse_query(query)
            
            # Perform conversion
            result = self._convert(value, from_unit, to_unit)
            
            # Format result
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            else:
                return str(round(result, 2))
                
        except Exception as e:
            raise ToolExecutionError(f"Unit conversion failed: {e}")
    
    def _parse_query(self, query: str) -> tuple[float, str, str]:
        """
        Parse conversion query to extract value and units.
        
        Args:
            query: Query string
            
        Returns:
            Tuple of (value, from_unit, to_unit)
        """
        query_lower = query.lower().strip()
        
        # Pattern: "convert X from_unit to to_unit"
        pattern = re.search(r'convert\s+(\d+(?:\.\d+)?)\s+(\w+)\s+to\s+(\w+)', query_lower)
        if pattern:
            value_str, from_unit, to_unit = pattern.groups()
            return float(value_str), from_unit.lower(), to_unit.lower()
        
        # Alternative pattern: "X from_unit to to_unit"
        pattern = re.search(r'(\d+(?:\.\d+)?)\s+(\w+)\s+to\s+(\w+)', query_lower)
        if pattern:
            value_str, from_unit, to_unit = pattern.groups()
            return float(value_str), from_unit.lower(), to_unit.lower()
        
        raise ValueError(f"Could not parse conversion query: {query}")
    
    def _convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Perform the actual unit conversion.
        
        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            Converted value
        """
        if from_unit == to_unit:
            return value
        
        # Look up conversion factor or function
        conversion_key = (from_unit, to_unit)
        if conversion_key not in self._conversions:
            raise ValueError(f"Cannot convert {from_unit} to {to_unit}")
        
        converter = self._conversions[conversion_key]
        
        if callable(converter):
            return converter(value)
        else:
            return value * converter
    
    def get_supported_units(self) -> Dict[str, list]:
        """Get list of supported unit types and their units."""
        units_by_type = {
            "currency": ["usd", "eur", "gbp"],
            "temperature": ["c", "f", "celsius", "fahrenheit"],
            "length": ["m", "ft", "km", "mi"],
            "weight": ["kg", "lb"]
        }
        return units_by_type


# Global instance
unitconv = UnitConverterTool()