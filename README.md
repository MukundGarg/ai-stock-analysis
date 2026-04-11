# 📊 StockSense AI - AI-Powered Stock Learning Platform

A full-stack AI application for analyzing financial documents and stock chart patterns.

## 🌟 Features

### PDF Financial Report Analyzer
- Upload and analyze financial reports (10-K, 10-Q, earnings calls)
- AI-powered insights using OpenAI GPT
- Get company summary, positives, risks, and future outlook
- Instant analysis in seconds

### Chart Pattern Analyzer
- Upload stock chart images (PNG/JPG)
- Detect 9 technical patterns:
  - Uptrend / Downtrend
  - Double Top / Double Bottom
  - Head and Shoulders
  - Triangles and Wedges
  - Flags
- Get Bullish/Bearish/Neutral signals with confidence levels

## 🚀 Quick Start

### Development Setup

**Prerequisites:**
- Node.js 20+
- Python 3.11+
- OpenAI API key

**1. Clone and Setup**
```bash
cd stocksense-ai
npm install
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Create Environment Files**

Frontend (.env.local):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend (.env):
```
OPENAI_API_KEY=sk-your-api-key
```

**3. Run Locally**

Terminal 1 - Backend:
```bash
cd backend
python main.py
```

Terminal 2 - Frontend:
```bash
npm run dev
```

Visit http://localhost:3000

---

## 📦 Tech Stack

**Frontend:**
- Next.js 16.2.3 (React 19)
- TypeScript
- TailwindCSS
- Deployed on Vercel

**Backend:**
- FastAPI (Python)
- OpenCV (computer vision)
- OpenAI API (AI analysis)
- Deployed on Render

---

## 🌐 Production Deployment

### Quick Deploy

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy Backend (Render)**
   - New Web Service
   - Connect GitHub repo
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Env: `OPENAI_API_KEY=sk-...`

3. **Deploy Frontend (Vercel)**
   - New Project
   - Connect GitHub repo
   - Env: `NEXT_PUBLIC_API_URL=https://backend-url`

### Full Deployment Guide
See [DEPLOYMENT.md](./DEPLOYMENT.md) for step-by-step instructions.

### Environment Variables Guide
See [ENV_VARIABLES.md](./ENV_VARIABLES.md) for all configuration options.

### Deployment Checklist
See [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) for verification steps.

---

## 📁 Project Structure

```
stocksense-ai/
├── app/                          # Next.js App Router
│   ├── page.tsx                  # Homepage
│   ├── features/page.tsx         # Features page
│   ├── dashboard/
│   │   ├── page.tsx              # Dashboard hub
│   │   ├── pdf/page.tsx          # PDF analyzer
│   │   ├── chart/page.tsx        # Chart analyzer
│   │   ├── sentiment/page.tsx    # Future
│   │   ├── simulator/page.tsx    # Future
│   │   └── movement/page.tsx     # Future
│   └── layout.tsx                # Root layout
│
├── components/                   # React components
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   ├── FeatureCard.tsx
│   └── ToolCard.tsx
│
├── backend/                      # FastAPI server
│   ├── main.py                   # API endpoints
│   ├── pdf_parser.py             # PDF processing
│   ├── ai_analyzer.py            # OpenAI integration
│   ├── chart_processor.py        # Image processing
│   ├── pattern_detector.py       # Pattern detection
│   ├── requirements.txt          # Python dependencies
│   └── .env.example             # Env template
│
├── public/                       # Static assets
├── vercel.json                  # Vercel config
├── Procfile                     # Render config
├── runtime.txt                  # Python version
├── package.json
└── tsconfig.json
```

---

## 🔌 API Endpoints

### POST /analyze-pdf
Analyze a financial report PDF.

**Request:**
```
POST /analyze-pdf
Content-Type: multipart/form-data
file: <PDF file>
```

**Response:**
```json
{
  "company_summary": "string",
  "key_positives": ["string", ...],
  "risks": ["string", ...],
  "future_outlook": "string"
}
```

### POST /analyze-chart
Analyze a stock chart image for patterns.

**Request:**
```
POST /analyze-chart
Content-Type: multipart/form-data
file: <PNG/JPG image>
```

**Response:**
```json
{
  "pattern": "string",
  "signal": "Bullish|Bearish|Neutral",
  "confidence": "High|Medium|Low",
  "description": "string"
}
```

### GET /health
Health check endpoint.

### GET /docs
Interactive API documentation (Swagger).

---

## 💡 Usage Examples

### Analyze a PDF
```bash
curl -X POST http://localhost:8000/analyze-pdf \
  -F "file=@financial-report.pdf"
```

### Analyze a Chart
```bash
curl -X POST http://localhost:8000/analyze-chart \
  -F "file=@chart.png"
```

---

## 🛠️ Development

### Frontend
- Run: `npm run dev`
- Build: `npm run build`
- Format: `npm run lint`

### Backend
- Run: `python backend/main.py`
- API Docs: http://localhost:8000/docs

---

## 📚 Documentation

- [Deployment Guide](./DEPLOYMENT.md) - Production deployment
- [Environment Variables](./ENV_VARIABLES.md) - All config options
- [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md) - Verification steps
- [Backend README](./backend/README.md) - Backend details

---

## 💾 Costs

| Component | Cost |
|-----------|------|
| Frontend (Vercel) | FREE |
| Backend (Render) | $7/month |
| OpenAI API | ~$0.01/analysis |
| **Total** | ~$8-17/month |

---

## 🤝 Contributing

Contributions welcome! Open an issue or submit a PR.

---

## 📄 License

MIT License - feel free to use for projects.

---

## 🚀 Deployed URLs (Example)

Once deployed:
- **Frontend:** https://stocksense-ai.vercel.app
- **Backend API:** https://stocksense-ai-backend.onrender.com
- **API Docs:** https://stocksense-ai-backend.onrender.com/docs

---

## ⚠️ Disclaimer

This platform provides educational insights only and does not constitute financial advice. Always do your own research and consult professionals before making investment decisions.

---

Ready to deploy? [See DEPLOYMENT.md](./DEPLOYMENT.md)
