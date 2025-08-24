"""
Tests for the main agent functionality.
"""
import pytest
from agent.agent import Agent, answer
from agent.models import ToolName


class TestAgent:
    """Test cases for the Agent class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = Agent()
    
    def test_calc_percent(self):
        """Test percentage calculations."""
        result = answer("What is 12.5% of 243?")
        assert result == "30.375"
    
    def test_weather_paris(self):
        """Test weather queries."""
        result = answer("What is the weather in Paris?")
        assert "C" in result
        assert "18" in result
    
    def test_kb_lovelace(self):
        """Test knowledge base queries."""
        result = answer("Who is Ada Lovelace?")
        assert "computing" in result.lower()
    
    def test_unitconv_usd_eur(self):
        """Test currency conversion."""
        result = answer("Convert 10 USD to EUR")
        assert result == "9"
    
    def test_unitconv_temp(self):
        """Test temperature conversion."""
        result = answer("Convert 100 C to F")
        assert result == "212"
    
    def test_complex_calculation(self):
        """Test complex calculation involving weather data."""
        result = answer("Add 10 to the average temperature in Paris and London right now.")
        # Paris: 18C, London: 17C, Average: 17.5C, +10 = 27.5C
        assert result == "27.5"
    
    def test_translation(self):
        """Test translation functionality."""
        # With quotes
        result = answer('Translate "hello" from English to Spanish')
        assert result == "hola"
        
        # Without quotes
        result = answer('Translate hello from English to Spanish')
        assert result == "hola"
    
    def test_empty_query(self):
        """Test handling of empty queries."""
        result = self.agent.answer("")
        assert "Please provide" in result
    
    def test_unknown_tool_graceful_fallback(self):
        """Test graceful handling of unknown queries."""
        result = self.agent.answer("What's the meaning of life?")
        # Should fallback to KB even if no exact match
        assert isinstance(result, str)
        assert len(result) > 0


class TestBackwardCompatibility:
    """Test backward compatibility with existing interface."""
    
    def test_answer_function_exists(self):
        """Test that the answer function still exists and works."""
        result = answer("What is 2 + 2?")
        assert result == "4"
    
    def test_calculator_basic(self):
        """Test basic calculator functionality."""
        assert answer("What is 5 + 3?") == "8"
        assert answer("What is 10 - 4?") == "6"
        assert answer("What is 3 * 7?") == "21"
        assert answer("What is 15 / 3?") == "5.0"
    
    def test_weather_different_cities(self):
        """Test weather for different cities."""
        paris_result = answer("Weather in Paris")
        london_result = answer("Weather in London")
        dhaka_result = answer("Weather in Dhaka")
        
        assert "18" in paris_result
        assert "17" in london_result
        assert "31" in dhaka_result
    
    def test_kb_different_people(self):
        """Test knowledge base for different people."""
        ada_result = answer("Who is Ada Lovelace?")
        alan_result = answer("Who is Alan Turing?")
        
        assert "computing" in ada_result.lower()
        assert "theoretical computer science" in alan_result.lower()


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = Agent()
    
    def test_invalid_calculation(self):
        """Test handling of invalid calculations."""
        result = self.agent.answer("What is 10 divided by zero?")
        assert "error" in result.lower() or "sorry" in result.lower()
    
    def test_unknown_city_weather(self):
        """Test weather query for unknown city."""
        result = answer("Weather in UnknownCity")
        # Should return default temperature
        assert "C" in result
    
    def test_invalid_unit_conversion(self):
        """Test invalid unit conversion."""
        result = answer("Convert 10 xyz to abc")
        assert "error" in result.lower() or "sorry" in result.lower()
    
    def test_malformed_query(self):
        """Test handling of malformed queries."""
        result = self.agent.answer("!!!@@@###")
        assert isinstance(result, str)
        assert len(result) > 0


class TestToolIntegration:
    """Test integration between different tools."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = Agent()
    
    def test_available_tools(self):
        """Test getting list of available tools."""
        tools = self.agent.get_available_tools()
        expected_tools = ["calculator", "weather", "kb", "unitconv", "translator"]
        
        for tool in expected_tools:
            assert tool in tools
            assert isinstance(tools[tool], str)
            assert len(tools[tool]) > 0
    
    def test_process_query_structured_response(self):
        """Test structured response from process_query."""
        response = self.agent.process_query("What is 2 + 2?")
        
        assert response.success is True
        assert response.result == "4"
        assert response.tool_used == ToolName.CALCULATOR
        assert response.error is None
    
    def test_process_query_error_response(self):
        """Test error response structure."""
        response = self.agent.process_query("")
        
        assert response.success is False
        assert response.error is not None
        assert "Empty query" in response.error