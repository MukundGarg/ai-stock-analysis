"""
StockSense AI Backend - FastAPI Server

Provides PDF and chart analysis endpoints for financial report processing.
"""

import os
import tempfile
from typing import Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import dotenv

from pdf_parser import extract_text_from_pdf, clean_and_truncate_text, get_pdf_metadata
from ai_analyzer import analyze_financial_report, create_fallback_analysis
from chart_processor import analyze_chart
from pattern_detector import detect_pattern
from news_fetcher import fetch_financial_news
from sentiment_analyzer import analyze_sentiment

# Load environment variables
dotenv.load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="StockSense AI Backend",
    description="Backend API for PDF financial report analysis",
    version="1.0.0"
)

# Configure CORS to allow requests from frontend
# Default: Allow localhost (development) + all vercel.app domains (production)
# Can be overridden with ALLOWED_ORIGINS environment variable
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", None)

if allowed_origins_env:
    # If explicitly set via environment variable, use those exact origins
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
    allow_origin_regex = None
else:
    # Default configuration: localhost for dev + regex for all vercel.app domains
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    allow_origin_regex = r"https://.*\.vercel\.app"

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class AnalysisResponse(BaseModel):
    """Response model for PDF analysis"""
    company_summary: str
    key_positives: list[str]
    risks: list[str]
    future_outlook: str


class ChartAnalysisResponse(BaseModel):
    """Response model for chart pattern analysis"""
    pattern: str
    signal: str
    confidence: str
    description: str


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    details: str | None = None


class SentimentRequest(BaseModel):
    """Request model for sentiment analysis"""
    query: str


class NewsArticle(BaseModel):
    """Model for news article in sentiment response"""
    title: str
    description: str | None = None
    source: str
    url: str
    published_at: str | None = None


class SentimentResponse(BaseModel):
    """Response model for sentiment analysis"""
    sentiment: str  # Bullish, Bearish, or Neutral
    sentiment_score: float  # -1.0 to 1.0
    summary: str  # AI-generated explanation
    key_reasons: list[str]  # Main themes from news
    news_sources: list[NewsArticle]  # Top news articles
    query: str  # Original user query


# Endpoints

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "StockSense AI Backend",
        "version": "1.0.0",
        "status": "running",
        "description": "AI-powered Stock Market Learning Platform Backend API",
        "endpoints": {
            "health": "/health (GET)",
            "analyze_pdf": "/analyze-pdf (POST)",
            "analyze_chart": "/analyze-chart (POST)",
            "analyze_sentiment": "/analyze-sentiment (POST)"
        },
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "service": "StockSense AI Backend",
        "version": "1.0.0"
    }


@app.post("/analyze-pdf", response_model=AnalysisResponse)
async def analyze_pdf(file: UploadFile = File(...)):
    """
    Analyze a PDF financial report.

    Accepts a PDF file and returns structured financial analysis.

    Args:
        file: PDF file upload

    Returns:
        AnalysisResponse with:
        - company_summary: Brief overview
        - key_positives: List of positive indicators
        - risks: List of risks
        - future_outlook: Growth assessment

    Raises:
        HTTPException: If file is invalid or analysis fails
    """

    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported. Please upload a .pdf file"
        )

    # Validate file size (max 25MB)
    file_size = 0
    content = await file.read()
    file_size = len(content)

    if file_size > 25 * 1024 * 1024:  # 25MB
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum size is 25MB"
        )

    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    temp_file_path = None

    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Extract text from PDF
        extracted_text, _ = extract_text_from_pdf(temp_file_path)

        if not extracted_text or len(extracted_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF. Please ensure it's a valid text-based PDF."
            )

        # Clean and truncate text for LLM
        cleaned_text = clean_and_truncate_text(extracted_text, max_length=8000)

        # Analyze with AI
        try:
            analysis = analyze_financial_report(cleaned_text)
        except ValueError as e:
            # If AI analysis fails, try fallback
            print(f"AI analysis failed: {str(e)}. Using fallback analysis.")
            analysis = create_fallback_analysis(cleaned_text)

        return AnalysisResponse(**analysis)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error analyzing PDF: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Server error during PDF analysis: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                print(f"Warning: Could not delete temporary file: {str(e)}")


@app.post("/analyze-chart", response_model=ChartAnalysisResponse)
async def analyze_chart_endpoint(file: UploadFile = File(...)):
    """
    Analyze a stock chart image for technical patterns.

    Accepts a chart image (PNG, JPG, JPEG) and returns detected patterns.

    Args:
        file: Chart image file upload

    Returns:
        ChartAnalysisResponse with:
        - pattern: Name of detected pattern
        - signal: Bullish/Bearish/Neutral
        - confidence: High/Medium/Low
        - description: Explanation of pattern

    Raises:
        HTTPException: If file is invalid or analysis fails
    """

    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    allowed_extensions = {".png", ".jpg", ".jpeg"}
    file_ext = os.path.splitext(file.filename.lower())[1]

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPG, and JPEG images are supported"
        )

    # Validate file size (max 5MB)
    content = await file.read()
    file_size = len(content)

    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum size is 5MB"
        )

    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    try:
        # Process the chart image
        analysis_data = analyze_chart(content)

        # Detect pattern from analysis
        pattern_result = detect_pattern(analysis_data)

        return ChartAnalysisResponse(**pattern_result)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error analyzing chart: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Server error during chart analysis: {str(e)}"
        )


@app.post("/analyze-sentiment", response_model=SentimentResponse)
async def analyze_sentiment_endpoint(request: SentimentRequest):
    """
    Analyze market sentiment based on user query using news and AI.

    Accepts a natural language query (e.g., "Why is the market falling?")
    and returns sentiment analysis with key reasons and relevant news articles.

    Args:
        request: Query request

    Returns:
        SentimentResponse with:
        - sentiment: Bullish, Bearish, or Neutral
        - sentiment_score: -1.0 to 1.0
        - summary: AI-generated explanation
        - key_reasons: Main themes from news
        - news_sources: Top 3-5 relevant articles

    Raises:
        HTTPException: If query is invalid, no news found, or analysis fails
    """

    # Validate query
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    if len(query) > 200:
        raise HTTPException(status_code=400, detail="Query cannot exceed 200 characters")

    try:
        # Fetch news articles
        print(f"[Sentiment] Fetching news for query: {query}")
        articles = await fetch_financial_news(query, max_articles=10)

        if not articles:
            raise HTTPException(
                status_code=404,
                detail=f"No news articles found for query: '{query}'. Try a different search term."
            )

        # Analyze sentiment
        print(f"[Sentiment] Analyzing sentiment for {len(articles)} articles")
        sentiment_analysis = analyze_sentiment(articles)

        # Select top 3-5 articles by recency
        top_articles = articles[:5]

        # Prepare news sources for response
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

        # Generate AI explanation using OpenAI
        print("[Sentiment] Generating AI explanation")
        ai_summary = await generate_sentiment_explanation(
            query=query,
            sentiment=sentiment_analysis["overall_sentiment"],
            sentiment_score=sentiment_analysis["sentiment_score"],
            key_reasons=sentiment_analysis["key_reasons"],
            articles=top_articles,
        )

        return SentimentResponse(
            sentiment=sentiment_analysis["overall_sentiment"],
            sentiment_score=sentiment_analysis["sentiment_score"],
            summary=ai_summary,
            key_reasons=sentiment_analysis["key_reasons"],
            news_sources=news_sources,
            query=query,
        )

    except HTTPException:
        raise
    except ValueError as e:
        print(f"[Sentiment] ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[Sentiment] Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Server error during sentiment analysis: {str(e)}"
        )


async def generate_sentiment_explanation(
    query: str,
    sentiment: str,
    sentiment_score: float,
    key_reasons: list[str],
    articles: list[dict],
) -> str:
    """
    Generate AI explanation for market sentiment using OpenAI.

    Args:
        query: Original user query
        sentiment: Bullish, Bearish, or Neutral
        sentiment_score: Sentiment score (-1.0 to 1.0)
        key_reasons: Main themes from news analysis
        articles: List of news articles

    Returns:
        AI-generated explanation string
    """

    # Prepare article summaries for context
    article_summaries = "\n".join(
        [f"- {article.get('title', '')}" for article in articles[:3]]
    )

    sentiment_prompt = f"""You are a financial analyst explaining market movements to beginners.

User Query: "{query}"

Current Market Sentiment:
- Overall Sentiment: {sentiment}
- Sentiment Score: {sentiment_score} (on scale -1 to 1)
- Key Themes: {', '.join(key_reasons)}

Recent News Headlines:
{article_summaries}

Based on this sentiment analysis and news context, provide a 2-3 sentence beginner-friendly explanation
of why the market or stock is moving. Be concise and focus on what matters for investment decisions.

Explanation:"""

    try:
        from ai_analyzer import get_openai_client
        client = get_openai_client()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful financial analyst explaining market movements to beginners. Keep explanations simple and brief (2-3 sentences).",
                },
                {"role": "user", "content": sentiment_prompt},
            ],
            temperature=0.7,
            max_tokens=300,
            timeout=30,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Fallback explanation if OpenAI fails
        print(f"[Sentiment] OpenAI API failed: {str(e)}. Using fallback explanation.")
        return fallback_sentiment_explanation(sentiment, key_reasons)


def fallback_sentiment_explanation(sentiment: str, key_reasons: list[str]) -> str:
    """
    Generate fallback explanation when OpenAI API fails.

    Args:
        sentiment: Bullish, Bearish, or Neutral
        key_reasons: Main themes

    Returns:
        Simple explanation based on sentiment
    """

    reasons_text = " and ".join(key_reasons) if key_reasons else "market conditions"

    if sentiment == "Bullish":
        return f"Market sentiment is positive based on recent news about {reasons_text}. Investors are optimistic about current market conditions."

    elif sentiment == "Bearish":
        return f"Market sentiment is negative due to concerns about {reasons_text}. Investors are cautious and concerned about market direction."

    else:
        return f"Market sentiment is neutral with mixed signals. Recent news suggests {reasons_text} are creating uncertainty in the market."


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )
