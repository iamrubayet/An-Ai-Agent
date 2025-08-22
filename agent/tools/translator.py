from typing import Dict, Any
from .base import BaseTool
from ..exceptions import ToolExecutionError, ValidationError


class TranslatorTool(BaseTool):
    """Tool for translating text between languages."""
    
    def __init__(self):
        # Mock translation dictionary - in production this would use a real translation API
        self._translations = {
            ("hello", "english", "spanish"): "hola",
            ("hello", "english", "french"): "bonjour",
            ("hello", "english", "german"): "hallo",
            ("hello", "english", "italian"): "ciao",
            ("goodbye", "english", "spanish"): "adiós",
            ("goodbye", "english", "french"): "au revoir",
            ("goodbye", "english", "german"): "auf wiedersehen",
            ("thank you", "english", "spanish"): "gracias",
            ("thank you", "english", "french"): "merci",
            ("thank you", "english", "german"): "danke",
            ("good morning", "english", "spanish"): "buenos días",
            ("good morning", "english", "french"): "bonjour",
            ("good morning", "english", "german"): "guten morgen",
            ("how are you", "english", "spanish"): "¿cómo estás?",
            ("how are you", "english", "french"): "comment allez-vous?",
            ("how are you", "english", "german"): "wie geht es ihnen?",
        }
        
        # Language codes mapping
        self._language_codes = {
            "en": "english", "eng": "english", "english": "english",
            "es": "spanish", "spa": "spanish", "spanish": "spanish",
            "fr": "french", "fra": "french", "french": "french",
            "de": "german", "ger": "german", "german": "german",
            "it": "italian", "ita": "italian", "italian": "italian",
        }
    
    @property
    def name(self) -> str:
        return "translator"
    
    def validate_args(self, args: Dict[str, Any]) -> None:
        """Validate translator arguments."""
        required_args = ["text", "from_lang", "to_lang"]
        for arg in required_args:
            if arg not in args:
                raise ValidationError(f"Translator requires '{arg}' argument")
            if not isinstance(args[arg], str):
                raise ValidationError(f"Argument '{arg}' must be a string")
    
    def execute(self, text: str, from_lang: str, to_lang: str, **kwargs) -> str:
        """
        Translate text between languages.
        
        Args:
            text: Text to translate
            from_lang: Source language
            to_lang: Target language
            
        Returns:
            Translated text
        """
        try:
            # Normalize language codes
            from_lang_norm = self._normalize_language(from_lang)
            to_lang_norm = self._normalize_language(to_lang)
            
            # Check if same language
            if from_lang_norm == to_lang_norm:
                return text
            
            # Normalize text for lookup
            text_norm = text.lower().strip()
            
            # Look up translation
            translation_key = (text_norm, from_lang_norm, to_lang_norm)
            
            if translation_key in self._translations:
                return self._translations[translation_key]
            
            # Fallback: mock translation by adding language suffix
            return f"{text} [{to_lang_norm}]"
            
        except Exception as e:
            raise ToolExecutionError(f"Translation failed: {e}")
    
    def _normalize_language(self, lang: str) -> str:
        """Normalize language code to full language name."""
        lang_lower = lang.lower().strip()
        return self._language_codes.get(lang_lower, lang_lower)
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages."""
        return ["english", "spanish", "french", "german", "italian"]
    
    def add_translation(self, text: str, from_lang: str, to_lang: str, translation: str) -> None:
        """
        Add a new translation to the dictionary.
        
        Args:
            text: Original text
            from_lang: Source language
            to_lang: Target language
            translation: Translated text
        """
        from_lang_norm = self._normalize_language(from_lang)
        to_lang_norm = self._normalize_language(to_lang)
        text_norm = text.lower().strip()
        
        key = (text_norm, from_lang_norm, to_lang_norm)
        self._translations[key] = translation


# Global instance
translator = TranslatorTool()