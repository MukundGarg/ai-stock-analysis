# StockSense AI Backend Documentation

## Overview

The backend is a FastAPI server that processes PDF financial reports and provides AI-powered analysis.

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── pdf_parser.py        # PDF text extraction logic
├── ai_analyzer.py       # OpenAI integration
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .env.example         # Example environment variables
└── venv/               # Python virtual environment
```

## Modules

### main.py
The main FastAPI application with:
- CORS configuration for frontend integration
- `/analyze-pdf` POST endpoint
- `/health` GET endpoint
- Exception handlers
- Error responses

### pdf_parser.py
PDF processing utilities:
- `extract_text_from_pdf()` - Extracts text from PDF files
- `clean_and_truncate_text()` - Cleans and limits text for LLM
- `get_pdf_metadata()` - Extracts PDF metadata

### ai_analyzer.py
AI analysis using OpenAI:
- `get_openai_client()` - Initialize OpenAI client
- `analyze_financial_report()` - Analyzes report text with GPT
- `create_fallback_analysis()` - Fallback analysis if API fails

## Installation

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 4. Run Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **pdfplumber**: PDF text extraction
- **openai**: OpenAI API client
- **python-multipart**: File upload support
- **pydantic**: Data validation
- **python-dotenv**: Environment variable management

See `requirements.txt` for versions.

## API Endpoints

### POST /analyze-pdf

Analyzes a PDF financial report.

**Parameters:**
- `file` (multipart/form-data): PDF file (max 25MB)

**Returns:**
```json
{
  "company_summary": "string",
  "key_positives": ["string", "string", "string"],
  "risks": ["string", "string", "string"],
  "future_outlook": "string"
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "error": "Only PDF files are supported..."
}
```

413 Payload Too Large:
```json
{
  "error": "File is too large. Maximum size is 25MB"
}
```

500 Internal Server Error:
```json
{
  "error": "Server error during PDF analysis..."
}
```

### GET /health

Health check endpoint.

**Returns:**
```json
{
  "status": "healthy",
  "service": "StockSense AI Backend",
  "version": "1.0.0"
}
```

### GET /docs

Interactive Swagger UI documentation.

Access at: http://localhost:8000/docs

### GET /

Root endpoint with service info.

## Configuration

### CORS Settings

The backend accepts requests from:
- http://localhost:3000
- http://127.0.0.1:3000
- http://0.0.0.0:3000

Modify in `main.py` if needed:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", ...],
    ...
)
```

### File Size Limits

- Maximum PDF size: 25MB
- Text truncation: 8000 characters

### API Limits

- Model: gpt-3.5-turbo (change in `ai_analyzer.py`)
- Temperature: 0.7
- Max tokens: 1000
- Timeout: 30 seconds

## How PDF Analysis Works

1. **File Validation**
   - Check file is PDF
   - Check file size < 25MB
   - Check file is not empty

2. **Text Extraction**
   - Use pdfplumber to extract text
   - Combine text from all pages
   - Handle extraction errors gracefully

3. **Text Cleaning**
   - Normalize whitespace
   - Truncate to 8000 characters (keeps important info within token limits)

4. **AI Analysis**
   - Send text to OpenAI GPT-3.5-turbo
   - Prompt extracts: summary, positives, risks, outlook
   - Parse JSON response
   - Validate structure

5. **Response**
   - Return structured JSON
   - HTTP 200 on success
   - HTTP 4xx/5xx on error

## Testing

### Test with cURL

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test API documentation
open http://localhost:8000/docs

# Test analysis endpoint
curl -X POST "http://localhost:8000/analyze-pdf" \
  -F "file=@/path/to/report.pdf"
```

### Using Swagger UI

Visit http://localhost:8000/docs in browser and use the "Try it out" button.

## Common Issues

### 1. ModuleNotFoundError

```
ModuleNotFoundError: No module named 'pdfplumber'
```

**Solution:**
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

### 2. OPENAI_API_KEY not set

```
ValueError: OPENAI_API_KEY environment variable not set
```

**Solution:**
1. Create `.env` file in backend folder
2. Add: `OPENAI_API_KEY=sk-...`
3. Restart server

### 3. Port already in use

```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Use different port
uvicorn main:app --port 8001

# Or kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### 4. PDF text extraction fails

```
"No text could be extracted from the PDF"
```

**Causes:**
- PDF is image-based (scanned)
- PDF is encrypted
- PDF is corrupted

**Solution:** Use a text-based PDF or OCR the image-based PDF first

### 5. OpenAI API errors

```
"OpenAI API error: ..."
```

**Causes:**
- Invalid API key
- API key quota exceeded
- API is down
- Network timeout

**Solution:**
- Verify API key at https://platform.openai.com/api-keys
- Check usage at https://platform.openai.com/usage
- Wait and retry

## Performance Optimization

### Reduce Analysis Time

**Option 1:** Use faster model (if available)
```python
model="gpt-3.5-turbo"  # Fast
model="gpt-4"          # Slower but better
```

**Option 2:** Reduce text length
```python
max_length=5000  # Instead of 8000
```

**Option 3:** Reduce AI response tokens
```python
max_tokens=500  # Instead of 1000
```

## Extending the Backend

### Add New Models

Edit `ai_analyzer.py`:
```python
response = client.chat.completions.create(
    model="your-model-here",
    ...
)
```

### Add PDF Metadata Extraction

Already available in `pdf_parser.py`:
```python
metadata = get_pdf_metadata(file_path)
```

### Add Result Caching

Could be added to avoid re-analyzing same PDFs:
```python
# Cache results in database or Redis
```

## Deployment

### Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t stocksense-pdf .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... stocksense-pdf
```

### Production Servers

- **Vercel/Heroku**: Use Dockerfile deployment
- **AWS/GCP/Azure**: Use container services
- **Traditional VPS**: Install Python and run with systemd/supervisor

## Architecture Notes

The system is designed to be:
- **Modular**: Separate concerns (PDF parsing, AI analysis)
- **Stateless**: No local state between requests
- **Scalable**: Can add caching, databases later
- **Maintainable**: Clear error handling and logging

## Future Enhancements

- Add database to store analysis history
- Implement caching for repeated analyses
- Add rate limiting
- Add user authentication
- Support multiple AI providers
- Add async processing for large files
- Implement webhooks for long-running jobs

---

**Version**: 1.0.0
**Status**: Production Ready
**Last Updated**: 2024
