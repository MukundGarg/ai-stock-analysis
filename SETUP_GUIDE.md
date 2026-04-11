# Stage 2 Setup Guide: PDF Financial Report Explainer

This guide will help you set up and run the PDF Financial Report Explainer feature with backend and frontend integration.

## Overview

The system consists of:
- **Frontend**: Next.js React component (already in project)
- **Backend**: FastAPI server with PDF processing and AI analysis
- **AI**: OpenAI GPT for financial report analysis

## Prerequisites

Before starting, make sure you have:
- Python 3.8+ installed
- Node.js/npm (already used for frontend)
- OpenAI API key (free or paid account)

## Step 1: Set Up OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new API key or use an existing one
3. Copy your API key

You'll need this for the environment setup below.

## Step 2: Install Backend Dependencies

Navigate to the backend folder and install Python dependencies:

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai/backend"
python -m venv venv
```

Activate the virtual environment:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Step 3: Set Environment Variables

Create a `.env` file in the backend folder:

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai/backend"
touch .env
```

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-api-key-here
```

Replace `sk-your-api-key-here` with your actual OpenAI API key.

## Step 4: Run the Backend Server

Make sure you're in the backend folder with the virtual environment activated:

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai/backend"
python main.py
```

You should see:
```
INFO:     Started server process [XXXX]
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The backend is now running at `http://localhost:8000`

Test it by visiting: http://localhost:8000/docs (API documentation)

## Step 5: Run the Frontend

In a new terminal, navigate to the frontend folder:

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai"
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Step 6: Test the Feature

1. Open http://localhost:3000/dashboard/pdf in your browser
2. Upload a PDF financial report (10-K, 10-Q, etc.)
3. Wait for the analysis to complete
4. View the results

## Troubleshooting

### Backend won't start

**Error: `ModuleNotFoundError`**
- Solution: Make sure you installed dependencies with `pip install -r requirements.txt`
- Solution: Make sure your virtual environment is activated

**Error: `OPENAI_API_KEY not set`**
- Solution: Create `.env` file with your API key
- Solution: Make sure you're running `python main.py` from the backend folder

### Frontend can't connect to backend

**Error: `Failed to fetch` or `Backend server not running`**
- Solution: Make sure backend is running on http://localhost:8000
- Solution: Check that CORS is enabled (it is in the code)
- Solution: Try accessing http://localhost:8000/health to verify backend is running

### PDF analysis fails

**Error: `No text could be extracted from PDF`**
- Solution: The PDF might be image-based or encrypted
- Solution: Try a different PDF file with text content

**Error: `OpenAI API error`**
- Solution: Check your API key is correct in `.env`
- Solution: Check you have API credits remaining (https://platform.openai.com/usage)
- Solution: The API might be rate-limited; wait a moment and try again

## API Reference

### POST /analyze-pdf

Analyzes a financial report PDF and returns structured insights.

**Request:**
```
POST http://localhost:8000/analyze-pdf
Content-Type: multipart/form-data

file: <PDF file>
```

**Response:**
```json
{
  "company_summary": "Brief company overview...",
  "key_positives": [
    "Positive indicator 1",
    "Positive indicator 2",
    "Positive indicator 3"
  ],
  "risks": [
    "Risk 1",
    "Risk 2",
    "Risk 3"
  ],
  "future_outlook": "Growth potential assessment..."
}
```

### GET /health

Health check endpoint.

**Request:**
```
GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "StockSense AI Backend",
  "version": "1.0.0"
}
```

### GET /docs

Interactive API documentation (Swagger UI)

Visit: http://localhost:8000/docs

## Example cURL Request

Test the API directly:

```bash
curl -X POST "http://localhost:8000/analyze-pdf" \
  -H "accept: application/json" \
  -F "file=@/path/to/your/report.pdf"
```

## Project Structure

```
stocksense-ai/
├── app/
│   └── dashboard/
│       └── pdf/
│           └── page.tsx           # Frontend component
├── backend/
│   ├── main.py                    # FastAPI server
│   ├── pdf_parser.py              # PDF text extraction
│   ├── ai_analyzer.py             # OpenAI integration
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables
│   └── venv/                      # Virtual environment
```

## How It Works

1. **Frontend** (Next.js)
   - User uploads a PDF
   - Component validates file
   - Sends POST request to backend with file

2. **Backend** (FastAPI)
   - Receives file upload
   - Extracts text using pdfplumber
   - Sends text to OpenAI GPT
   - Returns structured JSON

3. **Frontend Display**
   - Shows loading spinner while processing
   - Displays analysis results in 4 sections
   - Allows uploading another report

## Performance Notes

- **PDF Processing**: ~1-5 seconds depending on file size
- **OpenAI Analysis**: ~5-15 seconds depending on API load
- **Total Time**: ~10-20 seconds for typical financial reports

Larger PDFs may take longer.

## Next Steps After Stage 2

- Implement remaining tools (Chart Analyzer, Sentiment, etc.)
- Add database to store analysis history
- Add user authentication
- Create comparison features between multiple reports

## Support

Check the main README.md files for more information:
- `/StockSense_README.md` - Project overview
- `backend/` - Backend specific details

---

**Version**: 1.0.0
**Last Updated**: 2024
**Status**: Production Ready
