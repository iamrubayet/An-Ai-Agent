"""
Tests for the query planner.
"""
import pytest
from agent.planner import QueryPlanner
from agent.models import ToolName
from agent.exceptions import PlanningError


class TestQueryPlanner:
    """Test cases for the QueryPlanner class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.planner = QueryPlanner()
    
    def test_calculator_planning(self):
        """Test planning for calculator queries."""
        # Percentage calculations
        plan = self.planner.plan("What is 12.5% of 243?")
        assert plan.tool == ToolName.CALCULATOR
        assert plan.args["expr"] == "What is 12.5% of 243?"
        
        # Basic arithmetic
        plan = self.planner.plan("Add 10 to 5")
        assert plan.tool == ToolName.CALCULATOR
        assert plan.args["expr"] == "Add 10 to 5"
        
        # Mathematical operations
        plan = self.planner.plan("What is 2 + 2?")
        assert plan.tool == ToolName.CALCULATOR
        assert plan.args["expr"] == "What is 2 + 2?"
    
    def test_weather_planning(self):
        """Test planning for weather queries."""
        plan = self.planner.plan("What is the weather in Paris?")
        assert plan.tool == ToolName.WEATHER
        assert plan.args["city"] == "Paris"
        
        plan = self.planner.plan("Temperature in London")
        assert plan.tool == ToolName.WEATHER
        assert plan.args["city"] == "London"
        
        # Default city when not specified
        plan = self.planner.plan("What's the weather like?")
        assert plan.tool == ToolName.WEATHER
        assert "city" in plan.args
    
    def test_unit_conversion_planning(self):
        """Test planning for unit conversion queries."""
        plan = self.planner.plan("Convert 10 USD to EUR")
        assert plan.tool == ToolName.UNIT_CONVERTER
        assert plan.args["query"] == "Convert 10 USD to EUR"
        
        plan = self.planner.plan("Convert 100 C to F")
        assert plan.tool == ToolName.UNIT_CONVERTER
        assert plan.args["query"] == "Convert 100 C to F"
    
    def test_translation_planning(self):
        """Test planning for translation queries."""
        # With quotes and full specification
        plan = self.planner.plan('Translate "hello" from English to Spanish')
        assert plan.tool == ToolName.TRANSLATOR
        assert plan.args["text"] == "hello"
        assert plan.args["from_lang"] == "english"
        assert plan.args["to_lang"] == "spanish"
        
        # Without quotes and full specification
        plan = self.planner.plan('Translate hello from English to Spanish')
        assert plan.tool == ToolName.TRANSLATOR
        assert plan.args["text"] == "hello"
        assert plan.args["from_lang"] == "english"
        assert plan.args["to_lang"] == "spanish"
        
        # Simple translation pattern with quotes
        plan = self.planner.plan('Translate "goodbye" to French')
        assert plan.tool == ToolName.TRANSLATOR
        assert plan.args["text"] == "goodbye"
        assert plan.args["from_lang"] == "english"  # default
        assert plan.args["to_lang"] == "french"
        
        # Simple translation pattern without quotes
        plan = self.planner.plan('Translate goodbye to French')
        assert plan.tool == ToolName.TRANSLATOR
        assert plan.args["text"] == "goodbye"
        assert plan.args["from_lang"] == "english"  # default
        assert plan.args["to_lang"] == "french"
    
    def test_knowledge_base_planning(self):
        """Test planning for knowledge base queries."""
        plan = self.planner.plan("Who is Ada Lovelace?")
        assert plan.tool == ToolName.KNOWLEDGE_BASE
        assert plan.args["query"] == "Ada Lovelace"
        
        plan = self.planner.plan("What is machine learning?")
        assert plan.tool == ToolName.KNOWLEDGE_BASE
        assert plan.args["query"] == "What is machine learning?"
    
    def test_fallback_to_knowledge_base(self):
        """Test fallback to knowledge base for unknown queries."""
        plan = self.planner.plan("Tell me about quantum computing")
        assert plan.tool == ToolName.KNOWLEDGE_BASE
        assert plan.args["query"] == "Tell me about quantum computing"
    
    def test_case_insensitive_planning(self):
        """Test case insensitive query planning."""
        plan = self.planner.plan("WEATHER IN PARIS")
        assert plan.tool == ToolName.WEATHER
        assert plan.args["city"] == "Paris"  # Should be title case
        
        plan = self.planner.plan("convert 10 usd to eur")
        assert plan.tool == ToolName.UNIT_CONVERTER
    
    def test_complex_queries(self):
        """Test planning for complex queries."""
        # Query that could match multiple patterns - should prioritize calculator
        plan = self.planner.plan("Add 10 to the average temperature in Paris and London")
        assert plan.tool == ToolName.CALCULATOR
        
        # Translation with punctuation
        plan = self.planner.plan('Translate "How are you?" from English to German')
        assert plan.tool == ToolName.TRANSLATOR
        assert plan.args["text"] == "How are you?"
    
    def test_edge_cases(self):
        """Test edge cases in planning."""
        # Empty query
        plan = self.planner.plan("")
        assert plan.tool == ToolName.KNOWLEDGE_BASE
        
        # Whitespace only
        plan = self.planner.plan("   ")
        assert plan.tool == ToolName.KNOWLEDGE_BASE
        
        # Very short query
        plan = self.planner.plan("Hi")
        assert plan.tool == ToolName.KNOWLEDGE_BASE
    
    def test_planning_priority(self):
        """Test that planning follows correct priority order."""
        # Calculator should take priority over knowledge base for math
        plan = self.planner.plan("What is 5% of 100?")
        assert plan.tool == ToolName.CALCULATOR
        
        # Weather should take priority over knowledge base for weather queries
        plan = self.planner.plan("What's the temperature in Tokyo?")
        assert plan.tool == ToolName.WEATHER
        
        # Unit conversion should take priority over calculator
        plan = self.planner.plan("Convert 50 F to C")
        assert plan.tool == ToolName.UNIT_CONVERTER


class TestPlannerPatterns:
    """Test the regex patterns used in planning."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.planner = QueryPlanner()
    
    def test_percentage_pattern(self):
        """Test percentage pattern matching."""
        pattern = self.planner.patterns['percentage']
        
        assert pattern.search("12.5% of 243")
        assert pattern.search("50% of 100")
        assert pattern.search("0.5% of 1000")
        assert not pattern.search("50 percent of 100")
        assert not pattern.search("50% off")
    
    def test_city_extraction_pattern(self):
        """Test city name extraction pattern."""
        pattern = self.planner.patterns['city_extraction']
        
        match = pattern.search("weather in Paris")
        assert match and match.group(1).strip() == "Paris"
        
        match = pattern.search("temperature in New York")
        assert match and match.group(1).strip() == "New York"
        
        match = pattern.search("weather in London?")
        assert match and match.group(1).strip() == "London"
    
    def test_conversion_pattern(self):
        """Test conversion pattern matching."""
        pattern = self.planner.patterns['conversion']
        
        match = pattern.search("convert 10 usd to eur")
        assert match
        assert match.groups() == ("10", "usd", "eur")
        
        match = pattern.search("convert 100.5 c to f")
        assert match
        assert match.groups() == ("100.5", "c", "f")
    
    def test_translation_pattern(self):
        """Test translation pattern matching."""
        pattern = self.planner.patterns['translation']
        
        match = pattern.search('translate "hello" from english to spanish')
        assert match
        assert match.groups() == ("hello", "english", "spanish")
        
        match = pattern.search("translate 'goodbye' from french to german")
        assert match
        assert match.groups() == ("goodbye", "french", "german")
    
    def test_who_is_pattern(self):
        """Test 'who is' pattern matching."""
        pattern = self.planner.patterns['who_is']
        
        match = pattern.search("Who is Ada Lovelace?")
        assert match
        assert match.group(1).strip() == "Ada Lovelace"
        
        match = pattern.search("who is alan turing")
        assert match
        assert match.group(1).strip() == "alan turing"