from typing import Dict, Any
from .base import BaseTool
from ..exceptions import ToolExecutionError, ValidationError


class WeatherTool(BaseTool):
    """Tool for retrieving weather information."""
    
    def __init__(self):
        # Mock weather data - in production this would connect to a real API
        self._weather_data = {
            "paris": 18.0,
            "london": 17.0,
            "dhaka": 31.0,
            "amsterdam": 19.5,
            "new york": 22.0,
            "tokyo": 25.0,
            "berlin": 16.0,
            "sydney": 20.0,
        }
    
    @property
    def name(self) -> str:
        return "weather"
    
    def validate_args(self, args: Dict[str, Any]) -> None:
        """Validate weather arguments."""
        if "city" not in args:
            raise ValidationError("Weather tool requires 'city' argument")
        
        if not isinstance(args["city"], str):
            raise ValidationError("City must be a string")
    
    def execute(self, city: str, **kwargs) -> str:
        """
        Get weather information for a city.
        
        Args:
            city: City name
            
        Returns:
            Temperature information as string
        """
        try:
            normalized_city = city.strip().lower()
            
            if normalized_city in self._weather_data:
                temp = self._weather_data[normalized_city]
            else:
                # Default temperature for unknown cities
                temp = 20.0
            
            return f"{temp} C"
            
        except Exception as e:
            raise ToolExecutionError(f"Weather lookup failed: {e}")
    
    def get_temperature_value(self, city: str) -> float:
        """
        Get numeric temperature value for calculations.
        
        Args:
            city: City name
            
        Returns:
            Temperature as float
        """
        normalized_city = city.strip().lower()
        return self._weather_data.get(normalized_city, 20.0)


# Global instance
weather = WeatherTool()