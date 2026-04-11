# 🎯 START HERE - Stage 2: PDF Financial Report Explainer

Welcome! This guide will get you up and running in under 5 minutes.

## What Was Built

A complete PDF financial report analyzer with:
- **Frontend**: Next.js React component with file upload
- **Backend**: Python FastAPI server with PDF processing
- **AI**: OpenAI GPT-3.5-turbo for analysis
- **Results**: Structured insights (summary, positives, risks, outlook)

## 3 Simple Steps

### Step 1: Get OpenAI API Key (2 minutes)

1. Visit: https://platform.openai.com/api-keys
2. Sign up (free account available)
3. Create API key
4. Copy the key (starts with `sk-`)

### Step 2: Start Backend (1 minute)

Open Terminal and run:

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai/backend"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with API key
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

# Start server
python main.py
```

You should see: `Uvicorn running on http://0.0.0.0:8000`

### Step 3: Start Frontend (1 minute)

Open **another** Terminal and run:

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai"
npm run dev
```

You should see: `> ready - started server on 0.0.0.0:3000`

### Step 4: Use It! (1 minute)

1. Open browser: http://localhost:3000/dashboard/pdf
2. Upload a PDF financial report
3. Wait 15-20 seconds for AI analysis
4. View the results!

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Make sure venv is activated: `source venv/bin/activate` |
| Backend won't start | Use correct API key in `.env` file |
| `Failed to fetch` | Check backend is running on http://localhost:8000 |
| Out of API credits | Check https://platform.openai.com/usage |

## Where's Everything?

- **Frontend code**: `app/dashboard/pdf/page.tsx`
- **Backend code**: `backend/main.py`, `backend/pdf_parser.py`, `backend/ai_analyzer.py`
- **Setup guide**: `SETUP_GUIDE.md` (detailed with troubleshooting)
- **API docs**: `API_EXAMPLES.md` (how to use the API)
- **Quick start**: `QUICKSTART.md` (5-minute version)

## Key URLs

| URL | Purpose |
|-----|---------|
| http://localhost:3000/dashboard/pdf | PDF upload tool |
| http://localhost:8000/health | Check backend |
| http://localhost:8000/docs | API documentation |

## What Happens

1. You upload PDF
2. Frontend sends to backend
3. Backend extracts text from PDF
4. Backend sends to OpenAI GPT
5. GPT returns analysis
6. Frontend displays results

Total time: 15-20 seconds

## Next: Test With Real PDF

Download a financial report:
- https://www.sec.gov/cgi-bin/browse-edgar (search for companies)
- Look for 10-K or 10-Q files
- Download as PDF
- Upload to http://localhost:3000/dashboard/pdf

## Help

Need more details? Check these files:
- `SETUP_GUIDE.md` - Detailed setup with troubleshooting
- `QUICKSTART.md` - Quick reference
- `backend/README.md` - Backend documentation
- `API_EXAMPLES.md` - API usage examples
- `STAGE2_COMPLETE.md` - Full implementation details

## Ports

**Make sure these ports are free:**
- **3000** - Frontend (Next.js)
- **8000** - Backend (FastAPI)

If ports are busy, you'll get errors (see SETUP_GUIDE.md for solutions).

## What's Included

✅ Complete backend with:
- PDF text extraction
- OpenAI API integration
- Error handling
- CORS configuration

✅ Complete frontend with:
- Drag-and-drop file upload
- Loading states
- Results display
- Error messages
- Dark mode support
- Mobile responsive

✅ Full documentation with:
- Setup guide
- API examples
- Troubleshooting
- Architecture diagrams

## Success Looks Like

When it works, you'll see:
1. Upload screen with drag-and-drop
2. Loading spinner while analyzing
3. Four sections of results:
   - 📋 Company Summary
   - ✓ Key Positives
   - ⚠️ Risks  
   - 🔮 Future Outlook

## Common Questions

**Q: Do I need to pay for OpenAI?**
A: Free account gets $5 credits. Each analysis costs ~$0.01.

**Q: Does it work with image-based PDFs?**
A: No, PDFs must be text-based (not scanned images).

**Q: Can I save the results?**
A: Not yet - that's a future enhancement.

**Q: How long does analysis take?**
A: ~15-20 seconds per PDF.

## Architecture

```
Frontend (Next.js)           Backend (FastAPI)              OpenAI
    ↓                                ↓                        ↓
Upload PDF  →  POST /analyze-pdf  →  pdfplumber           GPT-3.5
              ← JSON Response     ←  extract text, analyze ←
Display Results
```

## File Structure

```
stocksense-ai/
├── app/dashboard/pdf/page.tsx       ← Frontend (UPDATED)
├── backend/                          ← Backend (NEW)
│   ├── main.py
│   ├── pdf_parser.py
│   ├── ai_analyzer.py
│   ├── requirements.txt
│   └── .env                          ← Create this
├── SETUP_GUIDE.md                   ← Read if stuck
├── QUICKSTART.md                    ← 5-min version
├── API_EXAMPLES.md                  ← API usage
└── STAGE2_COMPLETE.md               ← Full details
```

## What's Next

After testing, the next stages will add:
- Chart Pattern Analyzer
- Market Sentiment AI
- Trade Simulator
- Stock Movement Analysis

## Run Both Servers

**Pro Tip:** Use separate terminal tabs or windows:
- Tab 1: Backend (`python main.py`)
- Tab 2: Frontend (`npm run dev`)
- Tab 3: Testing/documentation

## Still Stuck?

1. Check `SETUP_GUIDE.md` - Most issues are there
2. Visit http://localhost:8000/docs - Interactive API docs
3. Check backend logs in terminal
4. Verify OpenAI API key is correct

## Ready? Let's Go! 🚀

Follow the 3 steps above, then visit:

**http://localhost:3000/dashboard/pdf**

Happy analyzing! 🎉

---

**Version**: 1.0.0
**Status**: Production Ready
**Made for**: StockSense AI
