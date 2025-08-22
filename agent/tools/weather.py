from typing import Dict, Any
from .base import BaseTool
from ..exceptions import ToolExecutionError, ValidationError


class WeatherTool(BaseTool):
    """Tool for retrieving weather information."""
    
    def __init__(self):
        # Mock weather data - in production this would connect to a real API
        self._weather_data = {
            "paris": {"temp": 18.0, "condition": "cloudy"},
            "london": {"temp": 17.0, "condition": "rainy"},
            "dhaka": {"temp": 31.0, "condition": "sunny"},
            "amsterdam": {"temp": 19.5, "condition": "partly cloudy"},
            "new york": {"temp": 22.0, "condition": "sunny"},
            "tokyo": {"temp": 25.0, "condition": "humid"},
            "berlin": {"temp": 16.0, "condition": "overcast"},
            "sydney": {"temp": 20.0, "condition": "clear"},
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
            Weather information as string
        """
        try:
            normalized_city = city.strip().lower()
            
            # Get weather data
            if normalized_city in self._weather_data:
                weather_info = self._weather_data[normalized_city]
                temp = weather_info["temp"]
                condition = weather_info["condition"]
            else:
                # Default weather for unknown cities
                temp = 20.0
                condition = "mild"
            
            # Check if this is a summary request (from the query context)
            query = kwargs.get("query", "").lower()
            if "summarize" in query and "words" in query:
                return self._generate_summary(temp, condition, query)
            
            # Default: return temperature
            return f"{temp} C"
            
        except Exception as e:
            raise ToolExecutionError(f"Weather lookup failed: {e}")
    
    def _generate_summary(self, temp: float, condition: str, query: str) -> str:
        """Generate a weather summary based on temperature and conditions."""
        # Determine temperature description
        if temp < 10:
            temp_desc = "cold"
        elif temp < 20:
            temp_desc = "mild"
        elif temp < 30:
            temp_desc = "warm"
        else:
            temp_desc = "hot"
        
        # Check if specific word count is requested
        import re
        word_match = re.search(r'(\d+)\s+words?', query)
        if word_match:
            word_count = int(word_match.group(1))
            if word_count == 3:
                return f"{temp_desc.title()} and {condition}."
            elif word_count == 2:
                return f"{temp_desc.title()} {condition}."
            elif word_count == 1:
                return temp_desc.title()
        
        # Default summary
        return f"{temp_desc.title()} and {condition}."
    
    def get_temperature_value(self, city: str) -> float:
        """
        Get numeric temperature value for calculations.
        
        Args:
            city: City name
            
        Returns:
            Temperature as float
        """
        normalized_city = city.strip().lower()
        if normalized_city in self._weather_data:
            return self._weather_data[normalized_city]["temp"]
        return 20.0


# Global instance
weather = WeatherTool()