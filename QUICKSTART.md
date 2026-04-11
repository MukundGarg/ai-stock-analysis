# 🚀 Quick Start: PDF Financial Report Explainer

Get the PDF Financial Report Explainer running in 5 minutes.

## Prerequisites

- OpenAI API key (get it free at https://platform.openai.com)
- Python 3.8+
- Node.js/npm (already installed)

## Quick Setup

### 1️⃣ Get OpenAI API Key

1. Visit https://platform.openai.com/api-keys
2. Create new API key
3. Copy the key (starts with `sk-`)

### 2️⃣ Set Up Backend (Terminal 1)

```bash
# Navigate to backend
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai/backend"

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

# Start server
python main.py
```

You should see:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3️⃣ Run Frontend (Terminal 2)

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai"
npm run dev
```

You should see:
```
> ready - started server on 0.0.0.0:3000
```

### 4️⃣ Test It

1. Open http://localhost:3000/dashboard/pdf
2. Upload a PDF (10-K, 10-Q, or any financial report)
3. Wait for AI analysis
4. View results!

## That's It! 🎉

You now have a working PDF analyzer.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Make sure venv is activated: `source venv/bin/activate` |
| `OPENAI_API_KEY not set` | Create `.env` file with your API key |
| `Failed to fetch` | Check backend is running on http://localhost:8000 |
| `No module named pdfplumber` | Run: `pip install -r requirements.txt` |

## Default Ports

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Stop Servers

Press `Ctrl+C` in each terminal to stop servers.

## Full Documentation

- Setup details: `SETUP_GUIDE.md`
- Backend docs: `backend/README.md`
- Project overview: `STOCKSENSE_README.md`

---

**Having issues?** Check SETUP_GUIDE.md for detailed troubleshooting.
