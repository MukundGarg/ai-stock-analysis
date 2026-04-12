"""
Vision-based chart analysis using OpenAI multimodal models — primary signal for patterns.
Falls back to CV pipeline when API fails.
"""

from __future__ import annotations

import base64
import io
import json
import os
import re
from typing import Any

from PIL import Image

from ai_analyzer import get_openai_client


def _image_mime_and_b64(image_bytes: bytes) -> tuple[str, str]:
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    raw = buf.getvalue()
    return "image/png", base64.standard_b64encode(raw).decode("ascii")


def analyze_chart_vision(image_bytes: bytes) -> dict[str, Any] | None:
    """
    Returns structured analysis or None on failure.
    Expected keys: pattern, signal, confidence_0_100, support_resistance, trendlines,
    breakout_notes, candlestick_notes, reasoning, beginner_explanation, caveats
    """
    try:
        mime, b64 = _image_mime_and_b64(image_bytes)
        client = get_openai_client()
        model = os.getenv("CHART_VISION_MODEL", "gpt-4o-mini")

        schema_hint = """Return ONLY valid JSON (no markdown) with exactly these keys:
{
  "pattern": "string — one of: Head and Shoulders, Inverse Head and Shoulders, Double Top, Double Bottom, Ascending Triangle, Descending Triangle, Symmetrical Triangle, Rising Wedge, Falling Wedge, Uptrend, Downtrend, Range / Rectangle, Breakout (up), Breakout (down), No clear pattern",
  "signal": "Bullish | Bearish | Neutral",
  "confidence_0_100": integer 0-100,
  "support_resistance": "1-3 sentences describing likely support/resistance zones or horizontal levels you see",
  "trendlines": "1-3 sentences about sloped trendlines if visible, else say not visible",
  "breakout_notes": "1-2 sentences on breakouts or false breakouts if any, else neutral",
  "candlestick_notes": "1-2 sentences on notable candlestick context if visible, else say unclear",
  "reasoning": "3-5 sentences: what you see in the chart and how you inferred the pattern (be honest if image is unclear)",
  "beginner_explanation": "2-4 sentences explaining the pattern in plain English for a beginner",
  "caveats": "1-2 sentences: image quality, timeframe unknown, not financial advice"
}"""

        prompt = f"""You are an experienced technical analyst helping Indian retail learners.
Analyze this price chart screenshot. Infer trend, support/resistance, trendlines, classic patterns (H&S, double top/bottom, triangles, wedges), and breakouts when plausible.
If the image is not a price chart or is too cluttered, set pattern to "No clear pattern", confidence_0_100 under 40, and explain why in reasoning.

{schema_hint}"""

        url = f"data:{mime};base64,{b64}"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": url, "detail": "high"}},
                    ],
                }
            ],
            temperature=0.2,
            max_tokens=900,
            timeout=90,
        )
        raw = (response.choices[0].message.content or "").strip()
        data = _parse_json_loose(raw)
        if not data:
            return None
        return _normalize_vision_payload(data)
    except Exception as e:
        print(f"[chart_vision] failed: {e}")
        return None


def _parse_json_loose(text: str) -> dict[str, Any] | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    m2 = re.search(r"\{[\s\S]*\}", text)
    if m2:
        try:
            return json.loads(m2.group(0))
        except json.JSONDecodeError:
            return None
    return None


def _normalize_vision_payload(data: dict[str, Any]) -> dict[str, Any]:
    conf = data.get("confidence_0_100", 50)
    try:
        conf = int(float(conf))
    except (TypeError, ValueError):
        conf = 50
    conf = max(0, min(100, conf))

    return {
        "pattern": str(data.get("pattern", "No clear pattern"))[:200],
        "signal": str(data.get("signal", "Neutral")),
        "confidence_0_100": conf,
        "support_resistance": str(data.get("support_resistance", ""))[:1200],
        "trendlines": str(data.get("trendlines", ""))[:1200],
        "breakout_notes": str(data.get("breakout_notes", ""))[:800],
        "candlestick_notes": str(data.get("candlestick_notes", ""))[:800],
        "reasoning": str(data.get("reasoning", ""))[:2000],
        "beginner_explanation": str(data.get("beginner_explanation", ""))[:1200],
        "caveats": str(data.get("caveats", ""))[:600],
        "source": "vision",
    }


def merge_vision_and_cv(vision: dict[str, Any] | None, cv_payload: dict[str, Any]) -> dict[str, Any]:
    """
    Produce API-facing chart result. Prefer vision when confidence is adequate.
    """
    if not vision:
        return cv_payload

    v_conf = vision.get("confidence_0_100", 0)
    cv_conf_map = {"High": 72, "Medium": 55, "Low": 38}
    cv_conf = cv_conf_map.get(str(cv_payload.get("confidence", "Low")), 40)

    use_vision = v_conf >= 45 or v_conf >= cv_conf

    if use_vision:
        conf_label = _score_to_label(v_conf)
        description_parts = [
            vision.get("beginner_explanation", ""),
            "",
            f"Support / resistance: {vision.get('support_resistance', '')}",
            f"Trendlines: {vision.get('trendlines', '')}",
            f"Breakouts: {vision.get('breakout_notes', '')}",
            f"Candles: {vision.get('candlestick_notes', '')}",
        ]
        if vision.get("caveats"):
            description_parts.append(f"Note: {vision.get('caveats')}")
        description = "\n".join(p for p in description_parts if p)

        return {
            "pattern": vision.get("pattern", cv_payload.get("pattern")),
            "signal": vision.get("signal", cv_payload.get("signal")),
            "confidence": conf_label,
            "confidence_score": v_conf,
            "description": description.strip(),
            "reasoning": vision.get("reasoning", ""),
            "support_resistance": vision.get("support_resistance", ""),
            "trendlines": vision.get("trendlines", ""),
            "breakout_notes": vision.get("breakout_notes", ""),
            "candlestick_notes": vision.get("candlestick_notes", ""),
            "beginner_explanation": vision.get("beginner_explanation", ""),
            "analysis_method": "vision_primary",
            "cv_fallback_summary": _cv_summary(cv_payload),
        }

    # Low vision confidence — blend textually
    return {
        **cv_payload,
        "confidence_score": cv_conf,
        "analysis_method": "cv_primary",
        "vision_secondary_note": vision.get("reasoning", "")[:500],
    }


def _score_to_label(score: int) -> str:
    if score >= 70:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def _cv_summary(cv: dict[str, Any]) -> str:
    return (
        f"Computer vision helper suggested “{cv.get('pattern')}” ({cv.get('signal')}, {cv.get('confidence')} confidence)."
    )
