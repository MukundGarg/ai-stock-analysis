"""
StockSense AI Backend — FastAPI: PDF, chart (vision + CV), sentiment, unified copilot.
"""

from __future__ import annotations

import os
import tempfile
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import dotenv

from ai_analyzer import analyze_financial_report, create_fallback_analysis
from chart_processor import analyze_chart
from chart_vision import analyze_chart_vision, merge_vision_and_cv
from copilot_service import copilot_chat
from indian_market_context import INDIAN_MARKETS_STRUCTURED
from news_fetcher import fetch_financial_news
from pdf_parser import clean_and_truncate_text, extract_text_from_pdf
from pattern_detector import detect_pattern
from sentiment_analyzer import analyze_sentiment, enrich_sentiment_with_llm

dotenv.load_dotenv()

app = FastAPI(
    title="StockSense AI Backend",
    description="Indian-market-focused trading copilot API",
    version="2.0.0",
)

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", None)

if allowed_origins_env:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
    allow_origin_regex = None
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    allow_origin_regex = r"https://.*\.vercel\.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExtractedDatum(BaseModel):
    label: str
    value_or_figure: str
    why_it_matters: str


class AnalysisResponse(BaseModel):
    summary: str
    key_insights: list[str]
    key_positives: list[str]
    risks: list[str]
    opportunities: list[str]
    important_extracted_data: list[ExtractedDatum]
    beginner_explanation: str
    company_summary: str
    future_outlook: str


class ChartAnalysisResponse(BaseModel):
    pattern: str
    signal: str
    confidence: str
    confidence_score: int = 0
    description: str
    reasoning: str = ""
    support_resistance: str = ""
    trendlines: str = ""
    breakout_notes: str = ""
    candlestick_notes: str = ""
    beginner_explanation: str = ""
    analysis_method: str = "cv_geometry"
    cv_fallback_summary: str | None = None
    vision_secondary_note: str | None = None


class SentimentRequest(BaseModel):
    query: str


class NewsArticle(BaseModel):
    title: str
    description: str | None = None
    source: str
    url: str
    published_at: str | None = None


class SentimentResponse(BaseModel):
    sentiment: str
    sentiment_score: float
    summary: str
    reasoning: str
    key_drivers: list[str]
    key_reasons: list[str]
    news_sources: list[NewsArticle]
    query: str


class CopilotRequest(BaseModel):
    message: str
    session_id: str | None = None
    workspace_context: dict[str, Any] | None = None


class CopilotResponse(BaseModel):
    reply: str
    session_id: str
    model: str


@app.get("/")
async def root():
    return {
        "name": "StockSense AI Backend",
        "version": "2.0.0",
        "status": "running",
        "description": "AI trading copilot API (Indian market focus)",
        "endpoints": {
            "health": "/health (GET)",
            "analyze_pdf": "/analyze-pdf (POST)",
            "analyze_chart": "/analyze-chart (POST)",
            "analyze_sentiment": "/analyze-sentiment (POST)",
            "copilot_chat": "/copilot/chat (POST)",
            "indian_markets": "/learn/indian-markets (GET)",
        },
        "documentation": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "StockSense AI Backend", "version": "2.0.0"}


@app.get("/learn/indian-markets")
async def learn_indian_markets():
    """Structured reference for UI and copilot onboarding."""
    return INDIAN_MARKETS_STRUCTURED


@app.post("/copilot/chat", response_model=CopilotResponse)
async def copilot_chat_endpoint(body: CopilotRequest):
    try:
        reply, sid, model = copilot_chat(
            body.message,
            body.session_id,
            body.workspace_context,
        )
        return CopilotResponse(reply=reply, session_id=sid, model=model)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        print(f"[copilot] error: {e}")
        raise HTTPException(status_code=500, detail="Copilot temporarily unavailable") from e


@app.post("/analyze-pdf", response_model=AnalysisResponse)
async def analyze_pdf(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    content = await file.read()
    if len(content) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File is too large (max 25MB)")
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        extracted_text, _ = extract_text_from_pdf(temp_file_path)
        if not extracted_text or not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted. Use a text-based PDF (not a scan without OCR).",
            )

        cleaned_text = clean_and_truncate_text(extracted_text, max_length=12000)

        try:
            analysis = analyze_financial_report(cleaned_text)
        except ValueError as e:
            print(f"AI analysis failed: {e}. Using fallback.")
            analysis = create_fallback_analysis(cleaned_text)

        return AnalysisResponse(**analysis)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Server error during PDF analysis: {e}") from e
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError as e:
                print(f"Warning: could not delete temp file: {e}")


@app.post("/analyze-chart", response_model=ChartAnalysisResponse)
async def analyze_chart_endpoint(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    allowed_extensions = {".png", ".jpg", ".jpeg"}
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only PNG, JPG, and JPEG images are supported")

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File is too large (max 5MB)")
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    try:
        vision = None
        try:
            vision = analyze_chart_vision(content)
        except Exception as e:
            print(f"[chart] vision skipped: {e}")

        analysis_data = analyze_chart(content)
        cv_payload = detect_pattern(analysis_data)
        merged = merge_vision_and_cv(vision, cv_payload)

        if merged.get("analysis_method") == "cv_primary":
            return ChartAnalysisResponse(
                pattern=str(merged.get("pattern", "")),
                signal=str(merged.get("signal", "Neutral")),
                confidence=str(merged.get("confidence", "Low")),
                confidence_score=int(merged.get("confidence_score", 0)),
                description=str(merged.get("description", "")),
                reasoning=str(merged.get("reasoning", "")),
                support_resistance=str(merged.get("support_resistance", "")),
                trendlines=str(merged.get("trendlines", "")),
                breakout_notes=str(merged.get("breakout_notes", "")),
                candlestick_notes=str(merged.get("candlestick_notes", "")),
                beginner_explanation=str(merged.get("beginner_explanation", "")),
                analysis_method=str(merged.get("analysis_method", "cv_geometry")),
                vision_secondary_note=merged.get("vision_secondary_note"),
            )

        return ChartAnalysisResponse(
            pattern=str(merged.get("pattern", "")),
            signal=str(merged.get("signal", "Neutral")),
            confidence=str(merged.get("confidence", "Low")),
            confidence_score=int(merged.get("confidence_score", 0)),
            description=str(merged.get("description", "")),
            reasoning=str(merged.get("reasoning", "")),
            support_resistance=str(merged.get("support_resistance", "")),
            trendlines=str(merged.get("trendlines", "")),
            breakout_notes=str(merged.get("breakout_notes", "")),
            candlestick_notes=str(merged.get("candlestick_notes", "")),
            beginner_explanation=str(merged.get("beginner_explanation", "")),
            analysis_method=str(merged.get("analysis_method", "vision_primary")),
            cv_fallback_summary=merged.get("cv_fallback_summary"),
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        print(f"Error analyzing chart: {e}")
        raise HTTPException(status_code=500, detail=f"Server error during chart analysis: {e}") from e


@app.post("/analyze-sentiment", response_model=SentimentResponse)
async def analyze_sentiment_endpoint(request: SentimentRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    if len(query) > 400:
        raise HTTPException(status_code=400, detail="Query cannot exceed 400 characters")

    try:
        articles = await fetch_financial_news(query, max_articles=10)
        if not articles:
            raise HTTPException(
                status_code=404,
                detail=f"No news articles found for: '{query}'. Try another phrase or check NEWSAPI_KEY.",
            )

        sentiment_analysis = analyze_sentiment(articles)
        top_articles = articles[:5]

        enriched = enrich_sentiment_with_llm(
            query=query,
            articles=top_articles,
            overall_sentiment=sentiment_analysis["overall_sentiment"],
            sentiment_score=sentiment_analysis["sentiment_score"],
            key_reasons=sentiment_analysis["key_reasons"],
        )

        ai_summary = await generate_sentiment_explanation(
            query=query,
            sentiment=sentiment_analysis["overall_sentiment"],
            sentiment_score=sentiment_analysis["sentiment_score"],
            key_reasons=enriched["key_drivers"],
            articles=top_articles,
        )

        news_sources = [
            NewsArticle(
                title=article.get("title", ""),
                description=article.get("description", ""),
                source=article.get("source", "Unknown"),
                url=article.get("url", ""),
                published_at=article.get("published_at", ""),
            )
            for article in top_articles
        ]

        return SentimentResponse(
            sentiment=sentiment_analysis["overall_sentiment"],
            sentiment_score=sentiment_analysis["sentiment_score"],
            summary=ai_summary,
            reasoning=enriched["reasoning"],
            key_drivers=enriched["key_drivers"],
            key_reasons=sentiment_analysis["key_reasons"],
            news_sources=news_sources,
            query=query,
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        print(f"[Sentiment] error: {e}")
        raise HTTPException(status_code=500, detail=f"Server error during sentiment analysis: {e}") from e


async def generate_sentiment_explanation(
    query: str,
    sentiment: str,
    sentiment_score: float,
    key_reasons: list[str],
    articles: list[dict],
) -> str:
    article_summaries = "\n".join([f"- {article.get('title', '')}" for article in articles[:3]])

    sentiment_prompt = f"""You are explaining market tone to **Indian retail investors** (NSE/BSE context).

User query: "{query}"

Sentiment label: {sentiment} (score {sentiment_score}, rough scale -1 to 1)
Key drivers: {', '.join(key_reasons)}

Headlines:
{article_summaries}

Write **2 short paragraphs** (beginner-friendly):
1) What the news flow suggests.
2) What to watch next and a reminder this is not investment advice.

Avoid buy/sell commands."""

    try:
        from ai_analyzer import get_openai_client

        client = get_openai_client()
        model = os.getenv("SENTIMENT_SUMMARY_MODEL", "gpt-4o-mini")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Clear, concise financial education for Indian readers. No markdown headings.",
                },
                {"role": "user", "content": sentiment_prompt},
            ],
            temperature=0.45,
            max_tokens=400,
            timeout=40,
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        print(f"[Sentiment] summary LLM failed: {e}")
        return fallback_sentiment_explanation(sentiment, key_reasons)


def fallback_sentiment_explanation(sentiment: str, key_reasons: list[str]) -> str:
    reasons_text = " and ".join(key_reasons) if key_reasons else "market conditions"
    if sentiment == "Bullish":
        return f"News tone looks constructive around {reasons_text}. Verify with primary sources before acting."
    if sentiment == "Bearish":
        return f"Headlines lean cautious on {reasons_text}. Risk sentiment can change quickly — read beyond titles."
    return f"Signals are mixed around {reasons_text}. Wait for clearer trend or dig into company-specific facts."


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
