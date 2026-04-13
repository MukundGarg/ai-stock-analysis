"""
Sentiment analysis — VADER baseline + Indian-market keyword themes + optional LLM synthesis.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

try:
    nltk.data.find("vader_lexicon")
except LookupError:
    nltk.download("vader_lexicon", quiet=True)

sia = SentimentIntensityAnalyzer()

# Lexical boosts for India-specific financial vocabulary (applied on top of VADER compound)
_INDIA_POS = {
    "nifty", "sensex", "record", "high", "upgrade", "beat", "growth", "inflows",
    "rate cut", "acquisition", "expansion", "guidance", "upside",
}
_INDIA_NEG = {
    "selloff", "crash", "scam", "fraud", "default", "outflows", "rate hike",
    "inflation", "slowdown", "ban", "probe", "penalty", "loss", "layoff",
}


def _india_lexical_adjustment(text: str) -> float:
    """Small delta in [-0.15, 0.15] based on India-relevant tokens."""
    t = text.lower()
    delta = 0.0
    for w in _INDIA_POS:
        if w in t:
            delta += 0.02
    for w in _INDIA_NEG:
        if w in t:
            delta -= 0.02
    return max(-0.15, min(0.15, delta))


def analyze_sentiment(articles: list[dict[str, Any]]) -> dict[str, Any]:
    """
    VADER per article + mild India keyword adjustment, then aggregate.
    """
    if not articles:
        return {
            "overall_sentiment": "Neutral",
            "sentiment_score": 0.0,
            "key_reasons": [],
            "article_sentiments": [],
        }

    article_sentiments: list[dict[str, Any]] = []
    scores: list[float] = []

    for article in articles:
        text_to_analyze = f"{article.get('title', '')} {article.get('description', '')}"
        if not text_to_analyze.strip():
            continue

        scores_dict = sia.polarity_scores(text_to_analyze)
        compound = scores_dict["compound"] + _india_lexical_adjustment(text_to_analyze)
        compound = max(-1.0, min(1.0, compound))
        scores.append(compound)

        if compound > 0.12:
            sentiment = "Bullish"
        elif compound < -0.12:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"

        article_sentiments.append(
            {
                "title": article.get("title", ""),
                "sentiment_score": round(compound, 3),
                "sentiment": sentiment,
            }
        )

    average_score = sum(scores) / len(scores) if scores else 0.0

    if average_score > 0.08:
        overall_sentiment = "Bullish"
    elif average_score < -0.08:
        overall_sentiment = "Bearish"
    else:
        overall_sentiment = "Neutral"

    key_reasons = extract_themes(articles)

    return {
        "overall_sentiment": overall_sentiment,
        "sentiment_score": round(average_score, 3),
        "key_reasons": key_reasons,
        "article_sentiments": article_sentiments,
    }


def extract_themes(articles: list[dict[str, Any]]) -> list[str]:
    """Theme buckets tuned for Indian equities + global macro spillovers."""
    theme_keywords: dict[str, list[str]] = {
        "rates_rbi": ["rbi", "repo", "rate hike", "rate cut", "liquidity", "mpc", "inflation", "cpi", "wpi"],
        "flows_fii_dii": ["fii", "dii", "foreign institutional", "inflows", "outflows", "fpi"],
        "india_indices": ["nifty", "sensex", "bank nifty", "banknifty", "midcap", "smallcap"],
        "currency_crude": ["rupee", "inr", "usd/inr", "forex", "crude", "oil", "brent"],
        "policy_sebi": ["sebi", "regulator", "circular", "compliance", "listing", "insider"],
        "earnings": ["earnings", "results", "quarter", "ebitda", "margin", "guidance", "profit", "revenue"],
        "growth": ["growth", "rally", "surge", "gain", "upgrade", "beat", "strong"],
        "stress": ["loss", "default", "downgrade", "selloff", "probe", "fraud", "warning", "ban"],
        "global_spillover": ["fed", "powell", "treasury", "us markets", "s&p", "nasdaq", "china", "europe"],
        "sector": ["bank", "it sector", "pharma", "auto", "metal", "real estate", "fmcg", "energy"],
    }

    theme_counts = {theme: 0 for theme in theme_keywords}
    combined_text = ""
    for article in articles:
        combined_text += f" {article.get('title', '')} {article.get('description', '')} "
    combined_text_lower = combined_text.lower()

    for theme, keywords in theme_keywords.items():
        for keyword in keywords:
            theme_counts[theme] += len(
                re.findall(r"\b" + re.escape(keyword) + r"\b", combined_text_lower)
            )

    sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
    top = [theme for theme, count in sorted_themes[:4] if count > 0]

    theme_descriptions = {
        "rates_rbi": "RBI / interest-rate and inflation narrative",
        "flows_fii_dii": "FII/DII flows and positioning",
        "india_indices": "Indian benchmark indices (Nifty/Sensex) tone",
        "currency_crude": "INR and crude — cost and macro pressure",
        "policy_sebi": "SEBI / policy / compliance headlines",
        "earnings": "Corporate earnings and results season",
        "growth": "Growth and positive momentum themes",
        "stress": "Credit, governance, or downside stress",
        "global_spillover": "Global markets and Fed/geopolitics spillover",
        "sector": "Sector-specific drivers",
    }

    readable = [theme_descriptions.get(theme, theme) for theme in top]
    if len(readable) < 2:
        readable.append("General market headlines and sentiment mix")
    return readable[:5]


def enrich_sentiment_with_llm(
    query: str,
    articles: list[dict[str, Any]],
    overall_sentiment: str,
    sentiment_score: float,
    key_reasons: list[str],
) -> dict[str, str]:
    """
    Produce reasoning + key_drivers tuned for Indian retail readers.
    Falls back to simple strings on error.
    """
    headlines = "\n".join(f"- {a.get('title', '')[:180]}" for a in articles[:6])
    try:
        from ai_provider import get_llm
        from ai_provider.config import get_provider_name

        llm = get_llm()
        if os.getenv("SENTIMENT_MODEL"):
            model = os.getenv("SENTIMENT_MODEL", "").strip()
        elif get_provider_name() == "groq":
            model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
        else:
            model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-002").strip()

        prompt = f"""User question: "{query}"

Headlines (sample):
{headlines}

Computed tone: {overall_sentiment} (score {sentiment_score} on approx -1..1 scale)
Theme buckets: {', '.join(key_reasons)}

Write for **Indian retail investors** (NSE/BSE context). 
Return ONLY valid JSON:
{{"reasoning": "3-5 sentences: what the news is saying, how it connects to India markets, uncertainties", "key_drivers": ["3-5 short bullets of concrete drivers"]}}
No buy/sell instructions; educational tone."""

        raw = llm.chat(
            [
                {"role": "system", "content": "JSON only. No markdown."},
                {"role": "user", "content": prompt},
            ],
            model=model,
            temperature=0.35,
            max_tokens=500,
        )
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            m = re.search(r"\{[\s\S]*\}", raw)
            if not m:
                raise
            data = json.loads(m.group(0))
        reasoning = str(data.get("reasoning", "")).strip()
        kd = data.get("key_drivers", [])
        if isinstance(kd, str):
            kd = [kd]
        key_drivers = [str(x) for x in kd][:6]
        if not key_drivers:
            key_drivers = list(key_reasons)[:5]
        return {"reasoning": reasoning, "key_drivers": key_drivers}
    except Exception as e:
        print(f"[sentiment] LLM enrich failed: {e}")
        return {
            "reasoning": (
                f"Headlines skew {overall_sentiment.lower()} for this query. "
                "This is an automated read of news tone — verify with primary sources and your own research."
            ),
            "key_drivers": list(key_reasons)[:5],
        }
