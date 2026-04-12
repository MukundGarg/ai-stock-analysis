"""
Pluggable LLM layer (Gemini or Groq). Configure with AI_PROVIDER + GEMINI_API_KEY or GROQ_API_KEY.
"""

from ai_provider.config import get_provider_name, is_llm_configured, require_config
from ai_provider.errors import LLMProviderError
from ai_provider.factory import get_llm, reset_llm_for_tests

__all__ = [
    "LLMProviderError",
    "get_llm",
    "is_llm_configured",
    "require_config",
    "get_provider_name",
    "reset_llm_for_tests",
]
