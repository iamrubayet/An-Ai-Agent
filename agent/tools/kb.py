import json
import os
from typing import Dict, Any
from .base import BaseTool
from ..exceptions import ToolExecutionError, ValidationError


class KnowledgeBaseTool(BaseTool):
    """Tool for looking up information from a knowledge base."""
    
    def __init__(self, kb_path: str = "data/kb.json"):
        self.kb_path = kb_path
        self._kb_data = None
        self._load_knowledge_base()
    
    @property
    def name(self) -> str:
        return "kb"
    
    def _load_knowledge_base(self) -> None:
        """Load knowledge base from file."""
        try:
            if os.path.exists(self.kb_path):
                with open(self.kb_path, "r", encoding="utf-8") as f:
                    self._kb_data = json.load(f)
            else:
                # Default knowledge base if file doesn't exist
                self._kb_data = {
                    "entries": [
                        {
                            "name": "Ada Lovelace",
                            "summary": "Ada Lovelace was a 19th-century mathematician regarded as an early computing pioneer for her work on Charles Babbage's Analytical Engine."
                        },
                        {
                            "name": "Alan Turing",
                            "summary": "Alan Turing was a mathematician and logician, widely considered to be the father of theoretical computer science and artificial intelligence."
                        }
                    ]
                }
        except Exception as e:
            # Initialize with empty knowledge base on error
            self._kb_data = {"entries": []}
    
    def validate_args(self, args: Dict[str, Any]) -> None:
        """Validate knowledge base arguments."""
        if "query" not in args:
            raise ValidationError("Knowledge base requires 'query' argument")
        
        if not isinstance(args["query"], str):
            raise ValidationError("Query must be a string")
    
    def execute(self, query: str, **kwargs) -> str:
        """
        Look up information in the knowledge base.
        
        Args:
            query: Search query
            
        Returns:
            Information from knowledge base or "No entry found"
        """
        try:
            if not self._kb_data or "entries" not in self._kb_data:
                return "Knowledge base is empty or corrupted"
            
            query_lower = query.lower().strip()
            
            # Search through entries
            for entry in self._kb_data.get("entries", []):
                name = entry.get("name", "").lower()
                summary = entry.get("summary", "")
                
                # Check if query matches name or is contained in name
                if query_lower in name or name in query_lower:
                    return summary
            
            return "No entry found."
            
        except Exception as e:
            raise ToolExecutionError(f"Knowledge base lookup failed: {e}")
    
    def add_entry(self, name: str, summary: str) -> None:
        """
        Add a new entry to the knowledge base.
        
        Args:
            name: Entry name
            summary: Entry summary/description
        """
        if not self._kb_data:
            self._kb_data = {"entries": []}
        
        if "entries" not in self._kb_data:
            self._kb_data["entries"] = []
        
        new_entry = {"name": name, "summary": summary}
        self._kb_data["entries"].append(new_entry)
    
    def save_knowledge_base(self) -> None:
        """Save knowledge base to file."""
        try:
            os.makedirs(os.path.dirname(self.kb_path), exist_ok=True)
            with open(self.kb_path, "w", encoding="utf-8") as f:
                json.dump(self._kb_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ToolExecutionError(f"Failed to save knowledge base: {e}")


# Global instance
kb = KnowledgeBaseTool()