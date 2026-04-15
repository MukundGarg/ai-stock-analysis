"""
AI Analyzer Module — structured PDF analysis via pluggable LLM (Gemini / Groq).
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

from ai_provider import get_llm, LLMProviderError
from ai_provider.config import get_provider_name
from ai_provider.constants import GEMINI_MODEL


def _sanitize_for_client(text: str, max_len: int = 600) -> str:
    t = re.sub(r"sk-[a-zA-Z0-9_-]{8,}", "[API key redacted]", text)
    t = re.sub(r"AIza[0-9A-Za-z_-]{20,}", "[API key redacted]", t)
    return t.strip()[:max_len]


def _http_status(exc: BaseException) -> int | None:
    return getattr(exc, "status_code", None) or getattr(exc, "status", None)


def _format_api_error(exc: BaseException) -> str:
    parts: list[str] = []
    st = _http_status(exc)
    if st is not None:
        parts.append(f"HTTP {st}")
    msg = getattr(exc, "message", None) or str(exc)
    if msg:
        parts.append(msg)
    body = getattr(exc, "body", None)
    if body is not None and str(body) not in msg:
        parts.append(str(body)[:400])
    return _sanitize_for_client(" — ".join(parts) if parts else str(exc))


def _should_try_next_model(exc: BaseException) -> bool:
    st = _http_status(exc)
    sfull = str(exc)
    if "429" in sfull or "503" in sfull:
        return True
    if st in (401, 403):
        return False
    if st == 429:
        return True
    if st is not None and 500 <= st < 600:
        return True
    if st == 404:
        return True
    low = str(exc).lower()
    if "model" in low and any(
        x in low for x in ("not found", "does not exist", "invalid", "unknown model", "does_not_exist")
    ):
        return True
    if "does not have access" in low:
        return True
    return False


def _pdf_model_pair() -> tuple[str, str]:
    """Primary and fallback model IDs for the active provider."""
    if get_provider_name() == "groq":
        primary = os.getenv("PDF_ANALYSIS_MODEL") or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        fallback = os.getenv("PDF_ANALYSIS_MODEL_FALLBACK", "llama-3.1-8b-instant")
    else:
        primary = os.getenv("PDF_ANALYSIS_MODEL") or os.getenv("GEMINI_MODEL", GEMINI_MODEL)
        fallback = os.getenv("PDF_ANALYSIS_MODEL_FALLBACK", GEMINI_MODEL)
    return primary.strip(), fallback.strip()


def analyze_financial_report(text: str) -> dict[str, Any]:
    """
    Analyze financial report text; return structured beginner-friendly output.
    Tries primary model then fallback when the failure looks retryable.
    """

    analysis_prompt = f"""You are an AI equity research analyst who explains corporate filings to investors.

Analyze the provided document and generate a concise financial analysis.

IMPORTANT RULES:
- Return ONLY valid JSON (no markdown, no headings, no text outside JSON)
- Do not include section titles or formatting
- All list fields must be arrays
- If no items exist for a list field, return empty array []
- Keep explanations brief (1-2 sentences)
- Facts must come only from the document
- Any speculation must be labeled "Possible"

Return JSON with exactly this structure:
{{
    "executive_summary": "1-2 sentence explanation of the filing",
    "ai_market_signal": {{
        "signal": "Bullish, Neutral, or Bearish",
        "confidence": number (0-100)
    }},
    "company_snapshot": "Brief explanation of what the company does and why this filing matters",
    "beginner_walkthrough": "Simple language explanation for beginner investors (2-3 sentences)",
    "key_insights": ["Important facts: company name, dates, stock symbols, regulatory references"],
    "strategic_intent": ["2-4 possible motives, each starting with 'Possible'"],
    "key_positives": ["2-4 strengths or positives from the filing"],
    "risks": ["2-4 potential risks related to the announcement"],
    "analyst_watchlist": ["3-5 key developments analysts will monitor"]
}}

Financial report excerpt:
{text}
"""

    llm = get_llm()
    primary, fb = _pdf_model_pair()
    models: list[str] = []
    for m in (primary, fb):
        if m and m not in models:
            models.append(m)

    print(f"[pdf] AI Provider: {get_provider_name()}")
    print(f"[pdf] Available models: {models}")
    print(f"[pdf] Primary model: {primary}")

    messages = [
        {"role": "system", "content": "You are a JSON-only API. You MUST respond with valid JSON only. Do not include any text outside the JSON. Do not use markdown code fences. Do not include headings or explanations. Return ONLY the JSON object."},
        {"role": "user", "content": analysis_prompt},
    ]

    for idx, model in enumerate(models):
        try:
            print(f"[pdf] Attempting analysis with model: {model}")
            response_text = llm.chat(
                messages,
                model=model,
                temperature=0.35,
                max_tokens=2200,
            )
            print(f"[pdf] Successfully received response from model: {model}")
            print(f"[pdf] Raw AI response (first 500 chars): {response_text[:500]}")
            analysis = _parse_json_response(response_text)
            print(f"[pdf] Successfully parsed JSON, keys: {list(analysis.keys())}")
            result = _validate_and_normalize_analysis(analysis)
            if model != primary:
                result["_pdf_model_used"] = model
            return result
        except LLMProviderError as e:
            print(f"[pdf] LLM error with model={model!r}: {_format_api_error(e)}")
            if idx < len(models) - 1 and _should_try_next_model(e):
                print(f"[pdf] Retrying with model={models[idx + 1]!r}")
                continue
            raise ValueError(f"LLM API error: {_format_api_error(e)}") from e
        except Exception as e:
            print(f"[pdf] Non-LLM error with model={model!r}: {e}")
            raise ValueError(f"Error analyzing report: {_sanitize_for_client(str(e))}") from e

    raise ValueError("No LLM models configured for PDF analysis.")


def sanitize_for_api_response(text: str, max_len: int = 600) -> str:
    return _sanitize_for_client(text, max_len)


def _parse_json_response(response_text: str) -> dict[str, Any]:
    """Parse JSON response using json.loads with safe fallback."""
    # Strip markdown code fences if present
    text = response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"[pdf] JSON parse error: {e}")
        print(f"[pdf] Attempted to parse: {text[:500]}")
        raise ValueError("Could not parse AI response as JSON") from None


def _validate_and_normalize_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize analysis with safe fallbacks for missing fields."""
    # Use safe fallbacks instead of raising errors
    result: dict[str, Any] = {
        "executive_summary": analysis.get("executive_summary", ""),
        "ai_market_signal": analysis.get("ai_market_signal", {
            "signal": "Neutral",
            "confidence": 50
        }),
        "company_snapshot": analysis.get("company_snapshot", ""),
        "beginner_walkthrough": analysis.get("beginner_walkthrough", ""),
        "key_insights": analysis.get("key_insights", []),
        "strategic_intent": analysis.get("strategic_intent", []),
        "key_positives": analysis.get("key_positives", []),
        "risks": analysis.get("risks", []),
        "analyst_watchlist": analysis.get("analyst_watchlist", []),
    }

    # Normalize list fields - ensure they are always arrays
    for list_key in ("strategic_intent", "key_insights", "key_positives", "risks", "analyst_watchlist"):
        if not isinstance(result[list_key], list):
            result[list_key] = [str(result[list_key])]
        result[list_key] = [str(x) for x in result[list_key]][:10]

    # Normalize ai_market_signal nested object
    if not isinstance(result["ai_market_signal"], dict):
        result["ai_market_signal"] = {
            "signal": "Neutral",
            "confidence": 50
        }
    else:
        # Support both old 'rating' and new 'signal' field names
        if "signal" not in result["ai_market_signal"]:
            result["ai_market_signal"]["signal"] = result["ai_market_signal"].get("rating", "Neutral")
        if "confidence" not in result["ai_market_signal"]:
            result["ai_market_signal"]["confidence"] = 50
        # Convert confidence to number
        try:
            result["ai_market_signal"]["confidence"] = int(result["ai_market_signal"]["confidence"])
        except (ValueError, TypeError):
            result["ai_market_signal"]["confidence"] = 50
        # Remove old fields if present
        result["ai_market_signal"].pop("rating", None)
        result["ai_market_signal"].pop("reason", None)

    # Limit text field lengths
    for text_key in ("executive_summary", "company_snapshot", "beginner_walkthrough"):
        result[text_key] = str(result[text_key])[:4000]

    return result


def classify_financial_analysis_error(exc: BaseException) -> str:
    msg = str(exc).lower()
    full = str(exc)
    if "not set" in msg and "key" in msg:
        return "missing_llm_key"
    if "llm api error" in msg:
        return "llm_error"
    if "401" in full or "403" in full:
        return "llm_error"
    if "429" in full or "quota" in msg or "rate" in msg:
        return "llm_error"
    if "json" in msg or "parse" in msg or "could not parse" in msg:
        return "json_parse"
    return "generic"


def create_fallback_analysis(
    text: str,
    *,
    reason_code: str | None = None,
) -> dict[str, Any]:
    summaries: dict[str, str] = {
        "missing_llm_key": (
            "Full AI analysis did not run because no LLM API key is configured on the server "
            "(GEMINI_API_KEY or GROQ_API_KEY, depending on AI_PROVIDER). "
            "Below is a basic keyword scan of the extracted text only."
        ),
        "missing_api_key": (
            "Full AI analysis did not run because no LLM API key is configured on the server. "
            "Below is a basic keyword scan of the extracted text only."
        ),
        "llm_error": (
            "Full AI analysis failed when calling the LLM from your host. "
            "See the technical detail below (billing, model name, or key). "
            "Below is a basic keyword scan of the extracted text only."
        ),
        "provider_error": (
            "Full AI analysis failed when calling the LLM. "
            "Below is a basic keyword scan of the extracted text only."
        ),
        "json_parse": (
            "The model returned text we could not parse as JSON. "
            "Below is a basic keyword scan of the extracted text only; try again or shorten the PDF."
        ),
        "generic": (
            "Full AI analysis could not complete. "
            "Below is a basic keyword scan of the extracted text only."
        ),
    }
    key = reason_code or "generic"
    summary = summaries.get(key, summaries["generic"])

    text_lower = text.lower()
    key_insights: list[str] = []
    risks: list[str] = []
    strategic_intent: list[str] = []

    if "revenue" in text_lower:
        key_insights.append("Revenue-related information appears in the document.")
    if "profit" in text_lower or "pat" in text_lower:
        key_insights.append("Profitability metrics appear in the excerpt.")
    if "debt" in text_lower or "borrowing" in text_lower:
        risks.append("Possible debt or leverage concerns.")
    if "litigation" in text_lower or "regulatory" in text_lower:
        risks.append("Possible legal or regulatory risks.")
    if "expansion" in text_lower or "capacity" in text_lower:
        strategic_intent.append("Possible expansion or capacity increase.")
    if "digital" in text_lower or "new product" in text_lower:
        strategic_intent.append("Possible new initiatives or product development.")

    while len(key_insights) < 3:
        key_insights.append("Review the full document for complete factual information.")
    while len(risks) < 3:
        risks.append("Review risk factors in the complete document.")
    while len(strategic_intent) < 3:
        strategic_intent.append("Possible strategic move requires full analysis.")

    return {
        "executive_summary": summary,
        "ai_market_signal": {
            "signal": "Neutral",
            "confidence": 50
        },
        "company_snapshot": "Company context requires full AI analysis or manual reading of the document.",
        "beginner_walkthrough": "Financial reports contain important company information. This automated view provides basic insights; enable AI for complete analysis.",
        "strategic_intent": strategic_intent[:4],
        "key_insights": key_insights[:5],
        "key_positives": ["Review the full document for complete positive insights."],
        "risks": risks[:4] if risks else ["No major risks detected in fallback mode."],
        "analyst_watchlist": [
            "Review revenue, margins, and cash flow trends.",
            "Monitor debt levels and covenants.",
            "Track management commentary on strategy."
        ]
    }
