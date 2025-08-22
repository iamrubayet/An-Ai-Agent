"""
Query planning and intent recognition.
"""
import re
from typing import Optional
from .models import ToolPlan, ToolName
from .exceptions import PlanningError
from .utils import normalize_text, log_execution_time


class QueryPlanner:
    """Handles query analysis and tool selection."""
    
    def __init__(self):
        self.patterns = self._init_patterns()
    
    def _init_patterns(self):
        """Initialize regex patterns for different query types."""
        return {
            'percentage': re.compile(r'\d+(?:\.\d+)?%\s+of\s+\d+(?:\.\d+)?'),
            'math_operations': re.compile(r'(?:add|subtract|multiply|divide|\+|\-|\*|\/|\d)'),
            'weather': re.compile(r'weather|temperature|temp'),
            'city_extraction': re.compile(r'in\s+([a-zA-Z\s]+?)(?:\s|$|\?|,)'),
            'conversion': re.compile(r'convert\s+(\d+(?:\.\d+)?)\s+(\w+)\s+to\s+(\w+)'),
            'translation': re.compile(r'translate\s+["\'](.+?)["\'].*?from\s+(\w+)\s+to\s+(\w+)'),
            'who_is': re.compile(r'who\s+is\s+(.+?)(?:\?|$)', re.IGNORECASE),
        }
    
    @log_execution_time
    def plan(self, query: str) -> ToolPlan:
        """
        Analyze query and create execution plan.
        
        Args:
            query: User query string
            
        Returns:
            ToolPlan with tool and arguments
            
        Raises:
            PlanningError: If query cannot be understood
        """
        normalized_query = normalize_text(query)
        original_query = query.strip()
        
        # Try each planning strategy
        planners = [
            self._plan_calculation,
            self._plan_unit_conversion,
            self._plan_translation,
            self._plan_weather,
            self._plan_knowledge_base,
        ]
        
        for planner in planners:
            try:
                plan = planner(normalized_query, original_query)
                if plan:
                    return plan
            except Exception as e:
                # Log but continue to next planner
                import logging
                logging.warning(f"Planner {planner.__name__} failed: {e}")
                continue
        
        # Fallback to knowledge base
        return ToolPlan(
            tool=ToolName.KNOWLEDGE_BASE,
            args={"query": original_query}
        )
    
    def _plan_calculation(self, normalized_query: str, original_query: str) -> Optional[ToolPlan]:
        """Plan for mathematical calculations."""
        # Check for percentage calculations
        if self.patterns['percentage'].search(normalized_query):
            return ToolPlan(
                tool=ToolName.CALCULATOR,
                args={"expr": original_query}
            )
        
        # Check for basic math operations
        if any(op in normalized_query for op in ['%', '+', '-', '*', '/', 'add', 'subtract', 'multiply', 'divide', 'average']):
            if self.patterns['math_operations'].search(normalized_query):
                return ToolPlan(
                    tool=ToolName.CALCULATOR,
                    args={"expr": original_query}
                )
        
        return None
    
    def _plan_unit_conversion(self, normalized_query: str, original_query: str) -> Optional[ToolPlan]:
        """Plan for unit conversions."""
        conversion_match = self.patterns['conversion'].search(normalized_query)
        if conversion_match:
            return ToolPlan(
                tool=ToolName.UNIT_CONVERTER,
                args={"query": original_query}
            )
        
        # Check for temperature and currency conversions
        if normalized_query.startswith('convert') and any(unit in normalized_query for unit in 
                                                        ['usd', 'eur', 'celsius', 'fahrenheit', 'c', 'f']):
            return ToolPlan(
                tool=ToolName.UNIT_CONVERTER,
                args={"query": original_query}
            )
        
        return None
    
    def _plan_translation(self, normalized_query: str, original_query: str) -> Optional[ToolPlan]:
        """Plan for text translation."""
        # Pattern 1: translate "text" from lang to lang (with quotes)
        translation_match = self.patterns['translation'].search(normalized_query)
        if translation_match:
            text, from_lang, to_lang = translation_match.groups()
            return ToolPlan(
                tool=ToolName.TRANSLATOR,
                args={
                    "text": text,
                    "from_lang": from_lang.lower(),
                    "to_lang": to_lang.lower()
                }
            )
        
        # Pattern 2: translate word from lang to lang (without quotes)
        unquoted_pattern = re.search(r'translate\s+(\w+)\s+from\s+(\w+)\s+to\s+(\w+)', normalized_query)
        if unquoted_pattern:
            text, from_lang, to_lang = unquoted_pattern.groups()
            return ToolPlan(
                tool=ToolName.TRANSLATOR,
                args={
                    "text": text,
                    "from_lang": from_lang.lower(),
                    "to_lang": to_lang.lower()
                }
            )
        
        # Pattern 3: translate "text" to lang (with quotes)
        simple_translate = re.search(r'translate\s+["\'](.+?)["\'].*?to\s+(\w+)', normalized_query)
        if simple_translate:
            text, to_lang = simple_translate.groups()
            return ToolPlan(
                tool=ToolName.TRANSLATOR,
                args={
                    "text": text,
                    "from_lang": "english",  # default
                    "to_lang": to_lang.lower()
                }
            )
        
        # Pattern 4: translate word to lang (without quotes)
        simple_unquoted = re.search(r'translate\s+(\w+)\s+to\s+(\w+)', normalized_query)
        if simple_unquoted:
            text, to_lang = simple_unquoted.groups()
            return ToolPlan(
                tool=ToolName.TRANSLATOR,
                args={
                    "text": text,
                    "from_lang": "english",  # default
                    "to_lang": to_lang.lower()
                }
            )
        
        return None
    
    def _plan_weather(self, normalized_query: str, original_query: str) -> Optional[ToolPlan]:
        """Plan for weather queries."""
        if self.patterns['weather'].search(normalized_query) or "summarize" in normalized_query:
            # Extract city name
            city_match = self.patterns['city_extraction'].search(normalized_query)
            city = city_match.group(1).strip().title() if city_match else "Paris"
            
            return ToolPlan(
                tool=ToolName.WEATHER,
                args={"city": city, "query": original_query}
            )
        
        return None
    
    def _plan_knowledge_base(self, normalized_query: str, original_query: str) -> Optional[ToolPlan]:
        """Plan for knowledge base queries."""
        # Who is queries
        who_match = self.patterns['who_is'].search(original_query)
        if who_match:
            person = who_match.group(1).strip()
            return ToolPlan(
                tool=ToolName.KNOWLEDGE_BASE,
                args={"query": person}
            )
        
        # General knowledge queries (fallback)
        if any(keyword in normalized_query for keyword in ['who', 'what', 'when', 'where', 'how']):
            return ToolPlan(
                tool=ToolName.KNOWLEDGE_BASE,
                args={"query": original_query}
            )
        
        return None