"""
AI Analyzer Module — OpenAI for PDF analysis and shared client access.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

from openai import OpenAI, APIError


def get_openai_client() -> OpenAI:
    """Get OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not set. "
            "Please set your OpenAI API key."
        )
    return OpenAI(api_key=api_key)


def analyze_financial_report(text: str) -> dict[str, Any]:
    """
    Analyze financial report text; return structured beginner-friendly output.
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

    client = get_openai_client()
    model = os.getenv("PDF_ANALYSIS_MODEL", "gpt-4o-mini")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You respond with valid JSON only. No markdown fences.",
                },
                {"role": "user", "content": analysis_prompt},
            ],
            temperature=0.35,
            max_tokens=2200,
            timeout=60,
        )
        response_text = (response.choices[0].message.content or "").strip()
        analysis = _parse_json_response(response_text)
        return _validate_and_normalize_analysis(analysis)
    except APIError as e:
        raise ValueError(f"OpenAI API error: {str(e)}") from e
    except Exception as e:
        raise ValueError(f"Error analyzing report: {str(e)}") from e


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
    """Return reason_code for create_fallback_analysis and API hints."""
    msg = str(exc).lower()
    full = str(exc)
    if "openai_api_key" in msg or "environment variable not set" in msg:
        return "missing_api_key"
    if "openai api error" in msg or "incorrect api key" in msg or "invalid_api_key" in msg:
        return "openai_error"
    if "rate limit" in msg or "429" in full:
        return "openai_error"
    if "json" in msg or "parse" in msg or "could not parse" in msg:
        return "json_parse"
    return "generic"


def create_fallback_analysis(
    text: str,
    *,
    reason_code: str | None = None,
) -> dict[str, Any]:
    """Structured fallback when the API is unavailable or fails."""

    summaries: dict[str, str] = {
        "missing_api_key": (
            "Full AI analysis did not run because the API server has no OpenAI key configured. "
            "Below is a basic keyword scan of the extracted text only."
        ),
        "openai_error": (
            "Full AI analysis failed due to an OpenAI API error (quota, billing, or network). "
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
    summary = summaries.get(reason_code or "generic", summaries["generic"])

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
