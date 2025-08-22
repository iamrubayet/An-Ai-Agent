"""
Tests for utility functions.
"""
import pytest
from agent.utils import safe_eval, normalize_text, extract_number_from_text


class TestSafeEval:
    """Test cases for safe_eval function."""
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic operations."""
        assert safe_eval("2 + 2") == 4
        assert safe_eval("10 - 3") == 7
        assert safe_eval("4 * 5") == 20
        assert safe_eval("15 / 3") == 5
        assert safe_eval("2 ** 3") == 8
        assert safe_eval("17 % 5") == 2
    
    def test_negative_numbers(self):
        """Test negative number handling."""
        assert safe_eval("-5") == -5
        assert safe_eval("-10 + 3") == -7
        assert safe_eval("5 + -3") == 2
    
    def test_floating_point(self):
        """Test floating point arithmetic."""
        assert safe_eval("3.5 + 2.1") == pytest.approx(5.6)
        assert safe_eval("10.0 / 4.0") == 2.5
        assert safe_eval("2.5 * 2") == 5.0
    
    def test_complex_expressions(self):
        """Test complex mathematical expressions."""
        assert safe_eval("(10 + 5) * 2") == 30
        assert safe_eval("100 / (5 + 5)") == 10
        assert safe_eval("2 + 3 * 4") == 14  # Order of operations
        assert safe_eval("(2 + 3) * 4") == 20
    
    def test_whitespace_handling(self):
        """Test whitespace handling in expressions."""
        assert safe_eval("  2 + 2  ") == 4
        assert safe_eval("10   -    3") == 7
        assert safe_eval("\t5 * 6\n") == 30
    
    def test_invalid_expressions(self):
        """Test handling of invalid expressions."""
        with pytest.raises(ValueError):
            safe_eval("import os")
        
        with pytest.raises(ValueError):
            safe_eval("2 + ")
        
        with pytest.raises(ValueError):
            safe_eval("2 ++ 3")
        
        with pytest.raises(ValueError):
            safe_eval("eval('2+2')")
    
    def test_unsupported_operations(self):
        """Test unsupported operations raise errors."""
        with pytest.raises(ValueError):
            safe_eval("2 & 3")  # Bitwise operations
        
        with pytest.raises(ValueError):
            safe_eval("2 << 1")  # Bit shifting
        
        with pytest.raises(ValueError):
            safe_eval("x = 5")  # Assignments
    
    def test_division_by_zero(self):
        """Test division by zero handling."""
        with pytest.raises(ValueError):
            safe_eval("10 / 0")
        
        with pytest.raises(ValueError):
            safe_eval("5 % 0")


class TestNormalizeText:
    """Test cases for normalize_text function."""
    
    def test_basic_normalization(self):
        """Test basic text normalization."""
        assert normalize_text("Hello World") == "hello world"
        assert normalize_text("  UPPER CASE  ") == "upper case"
        assert normalize_text("MiXeD cAsE") == "mixed case"
    
    def test_whitespace_handling(self):
        """Test whitespace normalization."""
        assert normalize_text("  leading spaces") == "leading spaces"
        assert normalize_text("trailing spaces  ") == "trailing spaces"
        assert normalize_text("  both ends  ") == "both ends"
        assert normalize_text("\tTabs and\nnewlines\r") == "tabs and\nnewlines"
    
    def test_empty_and_whitespace_only(self):
        """Test empty and whitespace-only strings."""
        assert normalize_text("") == ""
        assert normalize_text("   ") == ""
        assert normalize_text("\t\n\r ") == ""
    
    def test_special_characters(self):
        """Test handling of special characters."""
        assert normalize_text("Hello, World!") == "hello, world!"
        assert normalize_text("Question?") == "question?"
        assert normalize_text("Multiple   spaces") == "multiple   spaces"


class TestExtractNumberFromText:
    """Test cases for extract_number_from_text function."""
    
    def test_integer_extraction(self):
        """Test extraction of integers."""
        assert extract_number_from_text("There are 5 apples") == 5.0
        assert extract_number_from_text("Chapter 42") == 42.0
        assert extract_number_from_text("Year 2023") == 2023.0
    
    def test_float_extraction(self):
        """Test extraction of floating point numbers."""
        assert extract_number_from_text("Temperature is 23.5 degrees") == 23.5
        assert extract_number_from_text("Price: $19.99") == 19.99
        assert extract_number_from_text("Score: 98.7%") == 98.7
    
    def test_negative_numbers(self):
        """Test extraction of negative numbers."""
        assert extract_number_from_text("Temperature: -5.2°C") == -5.2
        assert extract_number_from_text("Loss of -10 points") == -10.0
    
    def test_first_number_only(self):
        """Test that only the first number is extracted."""
        assert extract_number_from_text("Buy 2 get 1 free") == 2.0
        assert extract_number_from_text("From 10 to 20 items") == 10.0
    
    def test_no_number_found(self):
        """Test handling when no number is found."""
        with pytest.raises(ValueError):
            extract_number_from_text("No numbers here")
        
        with pytest.raises(ValueError):
            extract_number_from_text("Just text and symbols!")
    
    def test_number_in_various_contexts(self):
        """Test number extraction in various contexts."""
        assert extract_number_from_text("Add 10 to the result") == 10.0
        assert extract_number_from_text("Convert 100 USD") == 100.0
        assert extract_number_from_text("What is 12.5% of something") == 12.5
    
    def test_edge_cases(self):
        """Test edge cases for number extraction."""
        assert extract_number_from_text("0.5 is a small number") == 0.5
        assert extract_number_from_text("Number: 0") == 0.0
        assert extract_number_from_text(".5 without leading zero") == 0.5