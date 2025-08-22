import pytest
from agent.tools.calculator import calculator
from agent.tools.weather import weather
from agent.tools.kb import kb
from agent.tools.unitconv import unitconv
from agent.tools.translator import translator
from agent.exceptions import ValidationError, ToolExecutionError


class TestCalculatorTool:
    """Test cases for the calculator tool."""
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic operations."""
        assert calculator.run(expr="2 + 2") == "4"
        assert calculator.run(expr="10 - 3") == "7"
        assert calculator.run(expr="4 * 5") == "20"
        assert calculator.run(expr="15 / 3") == "5"
    
    def test_percentage_calculation(self):
        """Test percentage calculations."""
        assert calculator.run(expr="What is 12.5% of 243?") == "30.375"
        assert calculator.run(expr="25% of 100") == "25.0"
        assert calculator.run(expr="50% of 200") == "100.0"
    
    def test_complex_expressions(self):
        """Test complex mathematical expressions."""
        assert calculator.run(expr="(10 + 5) * 2") == "30"
        assert calculator.run(expr="100 / (5 + 5)") == "10"
    
    def test_validation_error(self):
        """Test validation error handling."""
        with pytest.raises(ValidationError):
            calculator.run()  # No expr argument
        
        with pytest.raises(ValidationError):
            calculator.run(expr=123)  # Not a string
    
    def test_calculation_error(self):
        """Test calculation error handling."""
        with pytest.raises(ToolExecutionError):
            calculator.run(expr="invalid_expression")


class TestWeatherTool:
    """Test cases for the weather tool."""
    
    def test_known_cities(self):
        """Test weather for known cities."""
        assert weather.run(city="Paris") == "18.0 C"
        assert weather.run(city="London") == "17.0 C"
        assert weather.run(city="Dhaka") == "31.0 C"
    
    def test_case_insensitive(self):
        """Test case insensitive city names."""
        assert weather.run(city="PARIS") == "18.0 C"
        assert weather.run(city="london") == "17.0 C"
        assert weather.run(city="DhAkA") == "31.0 C"
    
    def test_unknown_city(self):
        """Test weather for unknown city."""
        result = weather.run(city="UnknownCity")
        assert "20.0 C" in result  # Default temperature
    
    def test_get_temperature_value(self):
        """Test getting numeric temperature values."""
        assert weather.get_temperature_value("Paris") == 18.0
        assert weather.get_temperature_value("London") == 17.0
        assert weather.get_temperature_value("UnknownCity") == 20.0
    
    def test_validation_error(self):
        """Test validation error handling."""
        with pytest.raises(ValidationError):
            weather.run()  # No city argument
        
        with pytest.raises(ValidationError):
            weather.run(city=123)  # Not a string


class TestKnowledgeBaseTool:
    """Test cases for the knowledge base tool."""
    
    def test_known_entries(self):
        """Test lookup of known entries."""
        result = kb.run(query="Ada Lovelace")
        assert "computing" in result.lower()
        assert "mathematician" in result.lower()
        
        result = kb.run(query="Alan Turing")
        assert "theoretical computer science" in result.lower()
    
    def test_case_insensitive_lookup(self):
        """Test case insensitive lookup."""
        result = kb.run(query="ada lovelace")
        assert "computing" in result.lower()
        
        result = kb.run(query="ALAN TURING")
        assert "theoretical computer science" in result.lower()
    
    def test_partial_name_match(self):
        """Test partial name matching."""
        result = kb.run(query="Lovelace")
        assert "computing" in result.lower()
        
        result = kb.run(query="Turing")
        assert "theoretical computer science" in result.lower()
    
    def test_unknown_entry(self):
        """Test lookup of unknown entry."""
        result = kb.run(query="Unknown Person")
        assert result == "No entry found."
    
    def test_validation_error(self):
        """Test validation error handling."""
        with pytest.raises(ValidationError):
            kb.run()  # No query argument
        
        with pytest.raises(ValidationError):
            kb.run(query=123)  # Not a string


class TestUnitConverterTool:
    """Test cases for the unit converter tool."""
    
    def test_currency_conversion(self):
        """Test currency conversions."""
        assert unitconv.run(query="Convert 10 USD to EUR") == "9.0"
        assert unitconv.run(query="Convert 100 EUR to USD") == "110.0"
    
    def test_temperature_conversion(self):
        """Test temperature conversions."""
        assert unitconv.run(query="Convert 100 C to F") == "212.0"
        assert unitconv.run(query="Convert 32 F to C") == "0.0"
    
    def test_length_conversion(self):
        """Test length conversions."""
        result = unitconv.run(query="Convert 1 M to FT")
        assert float(result) == pytest.approx(3.28, rel=0.1)
    
    def test_case_insensitive(self):
        """Test case insensitive unit names."""
        assert unitconv.run(query="convert 10 usd to eur") == "9.0"
        assert unitconv.run(query="convert 100 c to f") == "212.0"
    
    def test_alternative_patterns(self):
        """Test alternative query patterns."""
        assert unitconv.run(query="10 USD to EUR") == "9.0"
        assert unitconv.run(query="100 C to F") == "212.0"
    
    def test_unsupported_conversion(self):
        """Test unsupported unit conversion."""
        with pytest.raises(ToolExecutionError):
            unitconv.run(query="Convert 10 XYZ to ABC")
    
    def test_malformed_query(self):
        """Test malformed conversion query."""
        with pytest.raises(ToolExecutionError):
            unitconv.run(query="invalid conversion")
    
    def test_validation_error(self):
        """Test validation error handling."""
        with pytest.raises(ValidationError):
            unitconv.run()  # No query argument
        
        with pytest.raises(ValidationError):
            unitconv.run(query=123)  # Not a string
    
    def test_get_supported_units(self):
        """Test getting supported units."""
        units = unitconv.get_supported_units()
        assert "currency" in units
        assert "temperature" in units
        assert "length" in units
        assert "weight" in units


class TestTranslatorTool:
    """Test cases for the translator tool - NEW TOOL."""
    
    def test_basic_translation(self):
        """Test basic text translation."""
        result = translator.run(
            text="hello", 
            from_lang="english", 
            to_lang="spanish"
        )
        assert result == "hola"
        
        result = translator.run(
            text="goodbye", 
            from_lang="english", 
            to_lang="french"
        )
        assert result == "au revoir"
    
    def test_language_code_normalization(self):
        """Test language code normalization."""
        # Test with language codes
        result = translator.run(
            text="hello", 
            from_lang="en", 
            to_lang="es"
        )
        assert result == "hola"
        
        # Test with full names
        result = translator.run(
            text="hello", 
            from_lang="English", 
            to_lang="Spanish"
        )
        assert result == "hola"
    
    def test_same_language(self):
        """Test translation to same language."""
        result = translator.run(
            text="hello", 
            from_lang="english", 
            to_lang="english"
        )
        assert result == "hello"
    
    def test_unknown_translation(self):
        """Test translation of unknown text."""
        result = translator.run(
            text="unknown phrase", 
            from_lang="english", 
            to_lang="spanish"
        )
        # Should return fallback format
        assert "[spanish]" in result
    
    def test_supported_languages(self):
        """Test getting supported languages."""
        languages = translator.get_supported_languages()
        expected_languages = ["english", "spanish", "french", "german", "italian"]
        
        for lang in expected_languages:
            assert lang in languages
    
    def test_validation_errors(self):
        """Test validation error handling."""
        with pytest.raises(ValidationError):
            translator.run(text="hello", from_lang="english")  # Missing to_lang
        
        with pytest.raises(ValidationError):
            translator.run(from_lang="english", to_lang="spanish")  # Missing text
        
        with pytest.raises(ValidationError):
            translator.run(text=123, from_lang="english", to_lang="spanish")  # Invalid text type
    
    def test_add_translation(self):
        """Test adding new translations."""
        translator.add_translation(
            text="test phrase", 
            from_lang="english", 
            to_lang="spanish", 
            translation="frase de prueba"
        )
        
        result = translator.run(
            text="test phrase", 
            from_lang="english", 
            to_lang="spanish"
        )
        assert result == "frase de prueba"
    
    def test_case_insensitive_lookup(self):
        """Test case insensitive translation lookup."""
        result = translator.run(
            text="HELLO", 
            from_lang="ENGLISH", 
            to_lang="SPANISH"
        )
        assert result == "hola"
        
        result = translator.run(
            text="Hello", 
            from_lang="English", 
            to_lang="Spanish"
        )
        assert result == "hola"


class TestToolExtensibility:
    """Test that the tool system is extensible."""
    
    def test_all_tools_have_common_interface(self):
        """Test that all tools implement the common interface."""
        tools = [calculator, weather, kb, unitconv, translator]
        
        for tool in tools:
            # All tools should have these methods
            assert hasattr(tool, 'name')
            assert hasattr(tool, 'execute')
            assert hasattr(tool, 'validate_args')
            assert hasattr(tool, 'run')
            
            # Name should be a string
            assert isinstance(tool.name, str)
            assert len(tool.name) > 0
    
    def test_tool_validation_consistency(self):
        """Test that all tools validate their arguments consistently."""
        tools_and_invalid_args = [
            (calculator, {}),  # Missing expr
            (weather, {}),     # Missing city
            (kb, {}),          # Missing query
            (unitconv, {}),    # Missing query
            (translator, {}),  # Missing all required args
        ]
        
        for tool, invalid_args in tools_and_invalid_args:
            with pytest.raises(ValidationError):
                tool.validate_args(invalid_args)
    
    def test_new_tool_integration(self):
        """Test that the new translator tool integrates properly."""
        # Test that translator can be called like other tools
        result = translator.run(
            text="thank you", 
            from_lang="english", 
            to_lang="spanish"
        )
        assert result == "gracias"
        
        # Test error handling works the same way
        with pytest.raises(ValidationError):
            translator.run(text="hello")  # Missing required args