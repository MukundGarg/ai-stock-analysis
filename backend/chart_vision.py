"""
Vision-based chart analysis using the configured LLM (Gemini or Groq vision).
Falls back to CV pipeline when API fails.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

from ai_provider import get_llm
from ai_provider.config import is_llm_configured


def analyze_chart_vision(image_bytes: bytes) -> dict[str, Any] | None:
    """
    Returns structured analysis or None on failure.
    Expected keys: pattern, signal, confidence_0_100, support_resistance, trendlines,
    breakout_notes, candlestick_notes, reasoning, beginner_explanation, caveats
    """
    if not is_llm_configured():
        return None
    try:
        llm = get_llm()
        model = os.getenv("CHART_VISION_MODEL")
        if model:
            model = model.strip()

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
  "caveats": "1-2 sentences: image quality, timeframe unknown, not financial advice",
  "trade_setup": {
    "entry_zone": "Price area for entry (e.g., 'Near 4500-4550')",
    "stop_loss_zone": "Stop loss price area (e.g., 'Below 4450')",
    "target_1": "First target price",
    "target_2": "Second target price (if applicable)",
    "risk_reward_ratio": "string like '1:2.5' or '1:1.8'"
  },
  "pattern_quality": {
    "purity_score": integer 0-100,
    "false_signal_risk": "Low | Medium | High",
    "breakdown_continuation_probability": "Breakdown: X%, Continuation: Y%"
  },
  "market_context": {
    "current_trend": "Uptrend | Downtrend | Sideways",
    "market_structure_alignment": "Aligned | Neutral | Misaligned",
    "volatility_regime": "Low | Medium | High"
  },
  "confirmation": {
    "what_confirms": "What confirms the pattern (1-2 sentences)",
    "what_invalidates": "What invalidates the pattern (1-2 sentences)",
    "current_state": "Confirmed | Unconfirmed | Pending"
  },
  "scenarios": {
    "bull_case": "If pattern fails or reverses (1-2 sentences)",
    "bear_case": "If pattern confirms (1-2 sentences)",
    "neutral_case": "If consolidation or fakeout (1-2 sentences)"
  },
  "institutional_interpretation": {
    "institutional_action": "Would institutional traders act on this? (Yes/No/Maybe with brief reason)",
    "liquidity_hunt_risk": "Is this likely a liquidity hunt or stop trap? (Yes/No with brief reason)",
    "dominant_behavior": "Retail | Institutional | Mixed"
  }
}"""

        prompt = f"""You are a professional technical analyst providing trade decision intelligence for hedge funds and active traders.
Analyze this price chart screenshot with a trading-grade focus. Infer trend, support/resistance, trendlines, classic patterns (H&S, double top/bottom, triangles, wedges), and breakouts when plausible.
If the image is not a price chart or is too cluttered, set pattern to "No clear pattern", confidence_0_100 under 40, and explain why in reasoning.

CRITICAL: Focus on trade decision intelligence, not pattern explanation.
Provide specific entry zones, stop loss areas, targets, and risk-reward ratios.
Assess pattern quality, market context, and institutional interpretation.

MANDATORY INFERENCE RULES:
- If price scale is missing: INFER trade zones from relative structure (e.g., "Entry near neckline region", "Stop above swing high")
- NEVER output "N/A" for core trading fields
- Use labels: "Inferred (low confidence)", "Approximate zone based on structure", "Estimated based on swing geometry"
- Always generate ALL sections: trade_setup, pattern_quality, market_context, confirmation, scenarios, institutional_interpretation
- If data is missing: reduce confidence (e.g., 72→55) but NEVER remove output
- Scenarios MUST always be generated (label as "low confidence scenario modeling" if uncertain)

{schema_hint}"""

        raw = llm.vision_image(
            image_bytes,
            prompt,
            model=model,
            temperature=0.2,
            max_tokens=900,
        )
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

    # Normalize nested objects with inferred defaults
    trade_setup = data.get("trade_setup", {})
    if not isinstance(trade_setup, dict):
        trade_setup = {}
    trade_setup = {
        "entry_zone": str(trade_setup.get("entry_zone", "Inferred from chart structure"))[:200],
        "stop_loss_zone": str(trade_setup.get("stop_loss_zone", "Approximate zone based on swing geometry"))[:200],
        "target_1": str(trade_setup.get("target_1", "Estimated based on pattern projection"))[:200],
        "target_2": str(trade_setup.get("target_2", "Projected from pattern structure"))[:200],
        "risk_reward_ratio": str(trade_setup.get("risk_reward_ratio", "Estimated from structure"))[:50],
    }

    pattern_quality = data.get("pattern_quality", {})
    if not isinstance(pattern_quality, dict):
        pattern_quality = {}
    purity_score = pattern_quality.get("purity_score", 50)
    try:
        purity_score = int(float(purity_score))
    except (TypeError, ValueError):
        purity_score = 50
    purity_score = max(0, min(100, purity_score))
    pattern_quality = {
        "purity_score": purity_score,
        "false_signal_risk": str(pattern_quality.get("false_signal_risk", "Medium"))[:20],
        "breakdown_continuation_probability": str(pattern_quality.get("breakdown_continuation_probability", "Inferred from structure"))[:200],
    }

    market_context = data.get("market_context", {})
    if not isinstance(market_context, dict):
        market_context = {}
    market_context = {
        "current_trend": str(market_context.get("current_trend", "Inferred from swing structure"))[:20],
        "market_structure_alignment": str(market_context.get("market_structure_alignment", "Inferred"))[:20],
        "volatility_regime": str(market_context.get("volatility_regime", "Inferred from candle density"))[:20],
    }

    confirmation = data.get("confirmation", {})
    if not isinstance(confirmation, dict):
        confirmation = {}
    confirmation = {
        "what_confirms": str(confirmation.get("what_confirms", "Inferred from pattern structure"))[:400],
        "what_invalidates": str(confirmation.get("what_invalidates", "Based on swing invalidation logic"))[:400],
        "current_state": str(confirmation.get("current_state", "Inferred (low confidence)"))[:20],
    }

    scenarios = data.get("scenarios", {})
    if not isinstance(scenarios, dict):
        scenarios = {}
    scenarios = {
        "bull_case": str(scenarios.get("bull_case", "Low confidence scenario modeling"))[:400],
        "bear_case": str(scenarios.get("bear_case", "Low confidence scenario modeling"))[:400],
        "neutral_case": str(scenarios.get("neutral_case", "Low confidence scenario modeling"))[:400],
    }

    institutional_interpretation = data.get("institutional_interpretation", {})
    if not isinstance(institutional_interpretation, dict):
        institutional_interpretation = {}
    institutional_interpretation = {
        "institutional_action": str(institutional_interpretation.get("institutional_action", "Inferred from structure"))[:400],
        "liquidity_hunt_risk": str(institutional_interpretation.get("liquidity_hunt_risk", "Possible stop hunt inferred"))[:400],
        "dominant_behavior": str(institutional_interpretation.get("dominant_behavior", "Inferred from structure"))[:20],
    }

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
        "trade_setup": trade_setup,
        "pattern_quality": pattern_quality,
        "market_context": market_context,
        "confirmation": confirmation,
        "scenarios": scenarios,
        "institutional_interpretation": institutional_interpretation,
        "source": "vision",
    }


def merge_vision_and_cv(vision: dict[str, Any] | None, cv_payload: dict[str, Any]) -> dict[str, Any]:
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
