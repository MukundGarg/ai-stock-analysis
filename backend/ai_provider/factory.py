"""Factory for the active LLM provider."""

from __future__ import annotations

import os
from typing import Union

from ai_provider.config import get_provider_name, require_config
from ai_provider.errors import LLMProviderError
from ai_provider.gemini_provider import GeminiProvider
from ai_provider.groq_provider import GroqProvider

Provider = Union[GeminiProvider, GroqProvider]

_instance: Provider | None = None


def get_llm() -> Provider:
    """Singleton LLM facade (Gemini or Groq)."""
    global _instance
    if _instance is not None:
        return _instance
    require_config()
    name = get_provider_name()
    if name == "groq":
        key = (os.getenv("GROQ_API_KEY") or "").strip()
        if not key:
            raise ValueError("GROQ_API_KEY is empty.")
        _instance = GroqProvider(key)
    elif name == "gemini":
        key = (os.getenv("GEMINI_API_KEY") or "").strip()
        if not key:
            raise ValueError("GEMINI_API_KEY is empty.")
        _instance = GeminiProvider(key)
    else:
        raise LLMProviderError(
            f"Unknown AI_PROVIDER={name!r}. Use 'gemini' or 'groq'."
        )
    return _instance


def reset_llm_for_tests() -> None:
    global _instance
    _instance = None
