"""
LLM provider configuration.

Environment:
  AI_PROVIDER     — "gemini" (default) or "groq"
  GEMINI_API_KEY    — Google AI Studio key (https://aistudio.google.com/apikey)
  GROQ_API_KEY      — Groq API key (https://console.groq.com)

Model overrides (optional):
  GEMINI_MODEL, GEMINI_MODEL_FALLBACK
  GROQ_MODEL, GROQ_MODEL_FALLBACK
  COPILOT_MODEL, CHART_VISION_MODEL, PDF_ANALYSIS_MODEL, etc.
"""

from __future__ import annotations

import os


def get_provider_name() -> str:
    return (os.getenv("AI_PROVIDER", "gemini") or "gemini").strip().lower()


def is_llm_configured() -> bool:
    name = get_provider_name()
    if name == "groq":
        return bool((os.getenv("GROQ_API_KEY") or "").strip())
    if name == "gemini":
        return bool((os.getenv("GEMINI_API_KEY") or "").strip())
    return False


def require_config() -> None:
    if not is_llm_configured():
        name = get_provider_name()
        key = "GROQ_API_KEY" if name == "groq" else "GEMINI_API_KEY"
        raise ValueError(
            f"{key} is not set. Set AI_PROVIDER={name} and provide the matching API key."
        )
