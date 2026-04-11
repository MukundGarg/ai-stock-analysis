"""
StockSense AI Backend - FastAPI Server

Provides PDF analysis endpoint for financial report processing.
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

# Load environment variables
dotenv.load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="StockSense AI Backend",
    description="Backend API for PDF financial report analysis",
    version="1.0.0"
)

# Configure CORS to allow requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://0.0.0.0:3000",
    ],
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


@app.get("/health")
async def health_check():
    """Health check endpoint"""
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


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "StockSense AI Backend",
        "version": "1.0.0",
        "description": "AI-powered Stock Market Learning Platform API",
        "endpoints": {
            "health": "/health",
            "analyze_pdf": "/analyze-pdf (POST)",
            "analyze_chart": "/analyze-chart (POST)"
        },
        "docs": "/docs"
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Catch-all exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": str(exc)
        }
    )


# Run the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
