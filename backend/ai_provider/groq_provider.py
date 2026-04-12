"""Groq Cloud API (OpenAI-compatible) via httpx — no OpenAI SDK."""

from __future__ import annotations

import base64
import io
import os
from typing import Any

import httpx

from ai_provider.errors import LLMProviderError

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"


def _image_mime_and_b64(image_bytes: bytes) -> tuple[str, str]:
    from PIL import Image

    img = Image.open(io.BytesIO(image_bytes))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    raw = buf.getvalue()
    return "image/png", base64.standard_b64encode(raw).decode("ascii")


class GroqProvider:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            with httpx.Client(timeout=120.0) as client:
                r = client.post(
                    GROQ_CHAT_URL,
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                if r.status_code >= 400:
                    raise LLMProviderError(f"Groq HTTP {r.status_code}: {r.text[:800]}")
                return r.json()
        except httpx.RequestError as e:
            raise LLMProviderError(f"Groq connection error: {e}") from e

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        temperature: float = 0.5,
        max_tokens: int = 2048,
    ) -> str:
        model_name = (model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")).strip()
        # Groq expects OpenAI-style messages; string content only in this path
        oa_messages: list[dict[str, Any]] = []
        for m in messages:
            oa_messages.append({"role": m["role"], "content": m["content"]})
        data = self._post(
            {
                "model": model_name,
                "messages": oa_messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
        )
        try:
            return (data["choices"][0]["message"]["content"] or "").strip()
        except (KeyError, IndexError, TypeError) as e:
            raise LLMProviderError(f"Groq unexpected response: {data}") from e

    def vision_image(
        self,
        image_bytes: bytes,
        prompt: str,
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 900,
    ) -> str:
        mime, b64 = _image_mime_and_b64(image_bytes)
        url = f"data:{mime};base64,{b64}"
        model_name = (
            model
            or os.getenv("GROQ_VISION_MODEL")
            or os.getenv("CHART_VISION_MODEL")
            or "llama-3.2-11b-vision-preview"
        ).strip()
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": url}},
                ],
            }
        ]
        data = self._post(
            {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
        )
        try:
            return (data["choices"][0]["message"]["content"] or "").strip()
        except (KeyError, IndexError, TypeError) as e:
            raise LLMProviderError(f"Groq vision unexpected response: {data}") from e
