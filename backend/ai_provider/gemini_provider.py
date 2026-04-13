"""Google Gemini implementation using modern google-genai SDK."""

from __future__ import annotations

import os
from typing import Any

from google import genai
from google.genai import types

from ai_provider.constants import GEMINI_MODEL, GEMINI_VISION_MODEL
from ai_provider.errors import LLMProviderError


def _response_text(response: Any) -> str:
    try:
        if hasattr(response, "text"):
            return response.text.strip()
        if hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        return ""
    except Exception:
        return ""


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
        self.client = genai.Client(api_key=api_key)

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        temperature: float = 0.5,
        max_tokens: int = 2048,
    ) -> str:
        model_name = (model or os.getenv("GEMINI_MODEL", GEMINI_MODEL)).strip()
        print(f"[gemini] Using model: {model_name}")
        system, rest = _split_messages(messages)
        
        try:
            print(f"[gemini] Creating generation config")
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                system_instruction=system,
            )
            
            if len(rest) == 1 and rest[0].get("role") == "user":
                print(f"[gemini] Single message request")
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=rest[0]["content"],
                    config=config,
                )
                return _response_text(response)

            # Multi-turn chat
            print(f"[gemini] Multi-turn chat request")
            contents = []
            for m in rest:
                if m["role"] == "user":
                    contents.append(m["content"])
                elif m["role"] == "assistant":
                    contents.append({"role": "model", "parts": [m["content"]]})

            if not contents:
                raise LLMProviderError("No user message in chat request")

            response = self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            return _response_text(response)
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

        model_name = (model or os.getenv("GEMINI_VISION_MODEL") or os.getenv("CHART_VISION_MODEL") or GEMINI_VISION_MODEL).strip()
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            
            # Convert image to bytes for new SDK
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            response = self.client.models.generate_content(
                model=model_name,
                contents=[prompt, types.Part.from_bytes(data=img_bytes, mime_type="image/png")],
                config=config,
            )
            return _response_text(response)
        except Exception as e:
            raise LLMProviderError(f"Gemini vision error: {e}") from e
