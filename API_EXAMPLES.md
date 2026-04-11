# API Examples: PDF Financial Report Analyzer

Complete examples for testing the backend API.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Health Check

**Purpose**: Verify backend is running

**Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response (200):**
```json
{
  "status": "healthy",
  "service": "StockSense AI Backend",
  "version": "1.0.0"
}
```

### 2. Root Info

**Purpose**: Get API information

**Request:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response (200):**
```json
{
  "name": "StockSense AI Backend",
  "version": "1.0.0",
  "description": "PDF Financial Report Analysis API",
  "endpoints": {
    "health": "/health",
    "analyze_pdf": "/analyze-pdf (POST)"
  },
  "docs": "/docs"
}
```

### 3. Analyze PDF (Main Feature)

**Purpose**: Analyze a financial report PDF

**Request:**
```bash
curl -X POST "http://localhost:8000/analyze-pdf" \
  -H "accept: application/json" \
  -F "file=@/path/to/your/report.pdf"
```

**Request (using Python):**
```python
import requests

with open('report.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/analyze-pdf',
        files=files
    )

results = response.json()
print(results)
```

**Request (using JavaScript/Fetch):**
```javascript
const formData = new FormData();
formData.append('file', pdfFile);

const response = await fetch('http://localhost:8000/analyze-pdf', {
  method: 'POST',
  body: formData
});

const results = await response.json();
console.log(results);
```

**Successful Response (200):**
```json
{
  "company_summary": "Apple Inc. is a technology giant with strong financial performance, showing consistent revenue growth and healthy profit margins. The company maintains a dominant position in consumer electronics and services.",
  "key_positives": [
    "Strong revenue growth year-over-year",
    "High profit margins indicating pricing power",
    "Diversified revenue streams from hardware, software, and services",
    "Strong cash generation and balance sheet",
    "Growing services segment providing recurring revenue"
  ],
  "risks": [
    "Dependency on iPhone sales for core revenue",
    "Competitive pressure from other smartphone manufacturers",
    "Regulatory scrutiny on app store policies",
    "Supply chain vulnerabilities in Taiwan",
    "Saturation in developed markets limiting growth"
  ],
  "future_outlook": "Apple is well-positioned for continued growth through services expansion, emerging markets penetration, and new product categories like wearables and spatial computing. The company's strong brand and ecosystem lock-in support long-term value creation."
}
```

**Error Responses:**

```bash
# Invalid file type (400)
{
  "error": "Only PDF files are supported. Please upload a .pdf file"
}

# File too large (413)
{
  "error": "File is too large. Maximum size is 25MB"
}

# Empty file (400)
{
  "error": "File is empty"
}

# No text extractable (400)
{
  "error": "No text could be extracted from the PDF. Please ensure it's a valid text-based PDF."
}

# OpenAI API error (500)
{
  "error": "Server error during PDF analysis: OpenAI API error: ..."
}

# Backend not available (500)
{
  "error": "Internal server error",
  "details": "..."
}
```

## Testing in Swagger UI

1. Visit http://localhost:8000/docs
2. Click on `/analyze-pdf`
3. Click "Try it out"
4. Click "Choose Files" and select a PDF
5. Click "Execute"

## Test Files

You can test with these types of documents:

### Real SEC Filings
- Download from: https://www.sec.gov/cgi-bin/browse-edgar
- Files: 10-K (annual), 10-Q (quarterly), 8-K (current)

### Sample PDFs for Testing
```
Note: Make sure PDFs contain text (not scanned images)
```

## Response Format

All successful responses have this structure:

```json
{
  "company_summary": "string (2-3 sentences)",
  "key_positives": [
    "string",
    "string",
    "string"
  ],
  "risks": [
    "string",
    "string",
    "string"
  ],
  "future_outlook": "string (1-2 sentences)"
}
```

All lists contain up to 5 items.

## Error Response Format

```json
{
  "error": "Human-readable error message",
  "status_code": 400
}
```

## Rate Limiting

Currently no rate limiting. Plan for future:
- 10 requests per minute per IP
- 1 request per 5 seconds per API key

## Timeout

- File upload: 5 minutes
- PDF analysis: 30 seconds
- OpenAI API call: 30 seconds

Total time: ~10-20 seconds typical

## File Size Limits

- Maximum: 25 MB
- Recommended: < 10 MB
- Typical 10-K: 2-5 MB

## Text Processing

- Input text: Up to 8000 characters kept
- Output: JSON with structured analysis

## Common Integration Patterns

### Pattern 1: Simple Upload

```javascript
// User selects file
const file = document.getElementById('fileInput').files[0];

// Create form data
const formData = new FormData();
formData.append('file', file);

// Send request
const response = await fetch('http://localhost:8000/analyze-pdf', {
  method: 'POST',
  body: formData
});

if (response.ok) {
  const results = await response.json();
  displayResults(results);
} else {
  const error = await response.json();
  showError(error.error);
}
```

### Pattern 2: With Loading State

```javascript
setLoading(true);

try {
  const response = await fetch('http://localhost:8000/analyze-pdf', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) throw new Error('Analysis failed');

  const data = await response.json();
  setResults(data);
} catch (error) {
  setError(error.message);
} finally {
  setLoading(false);
}
```

### Pattern 3: File Validation Before Upload

```javascript
function validateFile(file) {
  // Check type
  if (file.type !== 'application/pdf') {
    return 'Only PDF files are supported';
  }

  // Check size (25MB = 25 * 1024 * 1024 bytes)
  if (file.size > 25 * 1024 * 1024) {
    return 'File must be smaller than 25MB';
  }

  return null; // Valid
}

const error = validateFile(file);
if (error) {
  showError(error);
  return;
}

// Proceed with upload
```

## Debugging

### Enable verbose logging

Edit `main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"  # Change to debug
    )
```

### Check request/response

```bash
# See full request/response with verbose curl
curl -v -X POST "http://localhost:8000/analyze-pdf" \
  -F "file=@report.pdf"
```

### Monitor backend

```bash
# Watch backend logs
tail -f backend.log

# Check open connections
netstat -an | grep 8000
```

## Performance Tips

1. **Optimize PDFs**: Compress PDFs before upload
2. **Batch Processing**: Don't upload very large documents
3. **Caching**: Frontend could cache results
4. **Async**: Backend is synchronous, could be made async

## Security Notes

- No authentication required (add in production)
- File size limits prevent abuse (25MB max)
- CORS allows only localhost
- No file storage (temporary files only)
- Sensitive data (API keys) in environment variables

## Migration to Production

1. Move API key to secrets manager
2. Add authentication/authorization
3. Implement rate limiting
4. Add request logging and monitoring
5. Use HTTPS
6. Add database for history
7. Consider async processing for large files

---

**Version**: 1.0.0
**Last Updated**: 2024
