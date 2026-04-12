"""Google Gemini implementation."""

from __future__ import annotations

import os
from typing import Any

import google.generativeai as genai

from ai_provider.errors import LLMProviderError


def _response_text(response: Any) -> str:
    try:
        return (response.text or "").strip()
    except Exception:
        parts = []
        for c in getattr(response, "candidates", []) or []:
            content = getattr(c, "content", None)
            if content and getattr(content, "parts", None):
                for p in content.parts:
                    if getattr(p, "text", None):
                        parts.append(p.text)
        return "\n".join(parts).strip()


def _split_messages(messages: list[dict[str, str]]) -> tuple[str | None, list[dict[str, str]]]:
    system_parts: list[str] = []
    rest: list[dict[str, str]] = []
    for m in messages:
        role = m.get("role", "")
        content = m.get("content", "")
        if role == "system":
            system_parts.append(content)
        else:
            rest.append({"role": role, "content": content})
    system = "\n\n".join(system_parts) if system_parts else None
    return system, rest


class GeminiProvider:
    def __init__(self, api_key: str) -> None:
        genai.configure(api_key=api_key)

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        temperature: float = 0.5,
        max_tokens: int = 2048,
    ) -> str:
        model_name = (model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")).strip()
        system, rest = _split_messages(messages)
        try:
            gen_model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system,
            )
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            if len(rest) == 1 and rest[0].get("role") == "user":
                resp = gen_model.generate_content(
                    rest[0]["content"],
                    generation_config=generation_config,
                )
                return _response_text(resp)

            history: list[dict[str, Any]] = []
            for m in rest[:-1]:
                if m["role"] == "user":
                    history.append({"role": "user", "parts": [m["content"]]})
                elif m["role"] == "assistant":
                    history.append({"role": "model", "parts": [m["content"]]})

            if not rest:
                raise LLMProviderError("No user message in chat request")

            last = rest[-1]
            if last.get("role") != "user":
                raise LLMProviderError("Last chat message must be from the user")

            chat = gen_model.start_chat(history=history)
            resp = chat.send_message(
                last["content"],
                generation_config=generation_config,
            )
            return _response_text(resp)
        except LLMProviderError:
            raise
        except Exception as e:
            raise LLMProviderError(f"Gemini API error: {e}") from e

    def vision_image(
        self,
        image_bytes: bytes,
        prompt: str,
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 900,
    ) -> str:
        import io

        from PIL import Image

        model_name = (model or os.getenv("GEMINI_VISION_MODEL") or os.getenv("CHART_VISION_MODEL") or "gemini-2.0-flash").strip()
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            gen_model = genai.GenerativeModel(model_name=model_name)
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            resp = gen_model.generate_content(
                [prompt, img],
                generation_config=generation_config,
            )
            return _response_text(resp)
        except Exception as e:
            raise LLMProviderError(f"Gemini vision error: {e}") from e
