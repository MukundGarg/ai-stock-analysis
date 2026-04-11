# 🔐 Environment Variables Guide

This file documents all environment variables needed for deployment.

## Frontend (Vercel)

### NEXT_PUBLIC_API_URL
- **What:** Backend API base URL
- **Format:** `https://stocksense-ai-backend.onrender.com` (production)
- **Where:** Vercel Settings → Environment Variables
- **Default:** `http://localhost:8000` (local development)
- **Required:** Yes (for production)

**Example for local development:**
```sh
# In .env.local (not committed)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Example for production:**
```sh
# In Vercel dashboard
NEXT_PUBLIC_API_URL=https://stocksense-ai-backend.onrender.com
```

---

## Backend (Render)

### OPENAI_API_KEY
- **What:** OpenAI API key for AI analysis
- **Format:** `sk-...` (starts with sk-)
- **Get:** https://platform.openai.com/api-keys
- **Where:** Render Environment Variables
- **Required:** Yes
- **Sensitive:** YES - Never commit or share!

**Example:**
```sh
OPENAI_API_KEY=sk-proj-abc123...
```

### ALLOWED_ORIGINS
- **What:** CORS allowed origins (comma-separated)
- **Format:** `https://stocksense-ai.vercel.app`
- **Where:** Render Environment Variables
- **Default:** `http://localhost:3000,http://localhost:3001,...` (local development)
- **Required:** Yes (for CORS to work in production)

**Example for local development:**
```sh
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000
```

**Example for production:**
```sh
ALLOWED_ORIGINS=https://stocksense-ai.vercel.app
```

---

## Setup Instructions

### Local Development

#### 1. Create Frontend .env.local
```bash
cd stocksense-ai
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

#### 2. Create Backend .env
```bash
cd backend
echo "OPENAI_API_KEY=sk-your-key-here" > .env
# Optional: Set local development origins
echo "ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001" >> .env
```

#### 3. Run Locally
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
npm run dev
```

---

### Production Deployment

#### 1. GitHub Push
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### 2. Render Backend Setup
- **Service Name:** `stocksense-ai-backend`
- **Environment Variables:**
  - `OPENAI_API_KEY` = sk-your-key
  - `ALLOWED_ORIGINS` = https://YOUR-VERCEL-DOMAIN.vercel.app

#### 3. Vercel Frontend Setup
- **Project Name:** `stocksense-ai`
- **Environment Variables:**
  - `NEXT_PUBLIC_API_URL` = https://stocksense-ai-backend.onrender.com

---

## Security Best Practices

### ✅ DO:
- ✅ Store `OPENAI_API_KEY` in Render secrets, never in code
- ✅ Use environment variables for all secrets
- ✅ Rotate API keys regularly
- ✅ Monitor OpenAI usage

### ❌ DON'T:
- ❌ Commit `.env` files to Git
- ❌ Share API keys in messages or PRs
- ❌ Use test/dummy API keys in production
- ❌ Expose API keys in frontend code

---

## Verifying Setup

### Check Frontend Environment Variable
```bash
# At build time, Vercel will show:
# Env vars imported at runtime: NEXT_PUBLIC_API_URL
```

### Check Backend Environment Variable
Only the backend logs will show if API key is loaded:
```
# In Render logs:
# INFO: Application startup complete
# API endpoint: /analyze-pdf
# API endpoint: /analyze-chart
```

---

## Troubleshooting

### "Backend server not running" Error
1. Check `NEXT_PUBLIC_API_URL` in Vercel settings
2. Verify it matches actual Render backend URL
3. Make sure backend is running (check Render logs)

### "OPENAI_API_KEY not set" Error
1. Check `OPENAI_API_KEY` is set in Render environment
2. Verify key format starts with `sk-`
3. Verify key has active usage permissions

### CORS Errors
1. Check exact Vercel frontend URL
2. Update `ALLOWED_ORIGINS` in Render to match
3. Redeploy Render service

---

## Reference

| Variable | Service | Type | Required |
|----------|---------|------|----------|
| NEXT_PUBLIC_API_URL | Vercel | Public | Yes (prod) |
| OPENAI_API_KEY | Render | Secret | Yes |
| ALLOWED_ORIGINS | Render | Env | Yes (prod) |

All set! 🚀
