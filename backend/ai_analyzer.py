"""
AI Analyzer Module — structured PDF analysis via pluggable LLM (Gemini / Groq).
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

from ai_provider import LLMProviderError, get_llm, get_provider_name


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
        primary = os.getenv("PDF_ANALYSIS_MODEL") or os.getenv("GEMINI_MODEL", "gemini-1.5-flash-002")
        fallback = os.getenv("PDF_ANALYSIS_MODEL_FALLBACK", "gemini-1.5-flash-002")
    return primary.strip(), fallback.strip()


def analyze_financial_report(text: str) -> dict[str, Any]:
    """
    Analyze financial report text; return structured beginner-friendly output.
    Tries primary model then fallback when the failure looks retryable.
    """

    analysis_prompt = f"""You are a financial analyst helping **Indian retail investors and beginners** understand company documents (annual reports, quarterly results, investor presentations, US-style 10-K/10-Q, or Indian filings).

Analyze the excerpt. If the document is not in INR, still explain clearly and mention currency when relevant.

Return ONLY valid JSON (no markdown) with exactly this structure:
{{
    "summary": "3-5 sentence executive summary in plain English",
    "key_insights": ["4-6 bullets of non-obvious insights from the text"],
    "key_positives": ["3-5 strengths or positives"],
    "risks": ["3-5 concrete risks or red flags"],
    "opportunities": ["3-5 growth or strategic opportunities mentioned or reasonably implied"],
    "important_extracted_data": [
        {{"label": "metric name", "value_or_figure": "number or range if present, else best textual value", "why_it_matters": "one sentence for beginners"}}
    ],
    "beginner_explanation": "Short paragraph explaining how to read this document and what a beginner should focus on next",
    "company_summary": "2-3 sentences: what the business does and scale/context",
    "future_outlook": "2-4 sentences on outlook, catalysts, and uncertainties"
}}

Rules:
- If a field has no basis in the text, write "Not clearly stated in excerpt" for that part rather than inventing numbers.
- Prefer actionable *education*, not buy/sell commands.
- Use simple language; avoid unexplained jargon.

Financial report excerpt:
{text}
"""

    llm = get_llm()
    primary, fb = _pdf_model_pair()
    models: list[str] = []
    for m in (primary, fb):
        if m and m not in models:
            models.append(m)

    messages = [
        {"role": "system", "content": "You respond with valid JSON only. No markdown fences."},
        {"role": "user", "content": analysis_prompt},
    ]

    for idx, model in enumerate(models):
        try:
            response_text = llm.chat(
                messages,
                model=model,
                temperature=0.35,
                max_tokens=2200,
            )
            analysis = _parse_json_response(response_text)
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
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        json_match = re.search(r"```(?:json)?\n?(.*?)\n?```", response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError("Could not parse AI response as JSON") from None


def _validate_and_normalize_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    required = [
        "summary",
        "key_insights",
        "key_positives",
        "risks",
        "opportunities",
        "important_extracted_data",
        "beginner_explanation",
        "company_summary",
        "future_outlook",
    ]
    for key in required:
        if key not in analysis:
            raise ValueError(f"AI response missing required field: {key}")

    for list_key in ("key_insights", "key_positives", "risks", "opportunities"):
        if not isinstance(analysis[list_key], list):
            analysis[list_key] = [str(analysis[list_key])]
        analysis[list_key] = [str(x) for x in analysis[list_key]][:8]

    raw_data = analysis["important_extracted_data"]
    normalized_data: list[dict[str, str]] = []
    if isinstance(raw_data, list):
        for item in raw_data[:12]:
            if isinstance(item, dict):
                normalized_data.append(
                    {
                        "label": str(item.get("label", "Item"))[:200],
                        "value_or_figure": str(item.get("value_or_figure", ""))[:300],
                        "why_it_matters": str(item.get("why_it_matters", ""))[:400],
                    }
                )
    analysis["important_extracted_data"] = normalized_data

    for text_key in ("summary", "beginner_explanation", "company_summary", "future_outlook"):
        analysis[text_key] = str(analysis[text_key])[:6000]

    return analysis


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
    key_positives: list[str] = []
    risks: list[str] = []
    opportunities: list[str] = []

    if "revenue" in text_lower and ("growth" in text_lower or "increase" in text_lower):
        key_positives.append("Revenue growth is mentioned in the document.")
    if "profit" in text_lower or "pat" in text_lower:
        key_positives.append("Profitability metrics appear in the excerpt.")
    if "ebitda" in text_lower or "margin" in text_lower:
        key_positives.append("Margin-related discussion is present — review trend vs prior periods.")

    if "loss" in text_lower:
        risks.append("Losses or negative results are referenced — read the full context.")
    if "debt" in text_lower or "borrowing" in text_lower:
        risks.append("Debt or leverage is mentioned — assess coverage and covenants in the full filing.")
    if "litigation" in text_lower or "regulatory" in text_lower:
        risks.append("Legal or regulatory items may need closer reading.")

    if "expansion" in text_lower or "capacity" in text_lower:
        opportunities.append("Expansion or capacity commentary may signal future revenue optionality.")
    if "digital" in text_lower or "new product" in text_lower:
        opportunities.append("New initiatives or digital themes are referenced.")

    while len(key_positives) < 3:
        key_positives.append("Review revenue, margins, and cash flow trends in the full report.")
    while len(risks) < 3:
        risks.append("Read risk factors and contingent liabilities in the complete document.")
    while len(opportunities) < 2:
        opportunities.append("Scan management discussion for strategy and capex plans.")

    return {
        "summary": summary,
        "key_insights": [
            "Fallback mode: insights are generic; enable AI for document-specific takeaways.",
            "Compare this period with the prior year and with peer companies in the same sector.",
            "Check cash flow vs profit — quality of earnings matters.",
        ],
        "key_positives": key_positives[:5],
        "risks": risks[:5],
        "opportunities": opportunities[:5],
        "important_extracted_data": [],
        "beginner_explanation": (
            "Financial reports are long on purpose. Start with the summary, key numbers, and risk section, "
            "then dig into notes. This automated view is educational, not advice."
        ),
        "company_summary": "Company context could not be reliably inferred in fallback mode.",
        "future_outlook": "Outlook requires full AI analysis or manual reading of management commentary.",
    }
