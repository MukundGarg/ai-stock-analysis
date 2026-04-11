# 🚀 Production Deployment Guide - StockSense AI

This guide walks you through deploying StockSense AI to production using **Vercel** (frontend) and **Render** (backend).

---

## Prerequisites

- ✅ GitHub account with code pushed
- ✅ OpenAI API key (from platform.openai.com)
- ✅ Vercel account (free tier available, sign up at vercel.com)
- ✅ Render account (free tier available, sign up at render.com)

---

## Overview

| Component | Platform | Cost | Status |
|-----------|----------|------|--------|
| Frontend (Next.js) | Vercel | Free | ✅ Ready |
| Backend (FastAPI) | Render | Free (then $7/month) | ✅ Ready |
| API Key | OpenAI | ~$0.01/analysis | ✅ Required |

---

## Part 1: Push Code to GitHub

### 1.1 Initialize Git (if not already done)

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai"
git init
git add .
git commit -m "Initial commit: StockSense AI full-stack application"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create repository named `stocksense-ai`
3. **Do not** initialize with README (we have one)

### 1.3 Push Code to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/stocksense-ai.git
git branch -M main
git push -u origin main
```

---

## Part 2: Deploy Backend to Render

### 2.1 Create Render Account

1. Go to https://render.com
2. Sign up (free tier available)
3. Connect GitHub account

### 2.2 Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Select your `stocksense-ai` GitHub repository
3. Fill in the form:
   - **Name:** `stocksense-ai-backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free (startup - auto-scales on demand)

### 2.3 Set Environment Variables

In Render dashboard, **Environment** tab, add:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
ALLOWED_ORIGINS=https://YOUR-FRONTEND-URL.vercel.app
```

Replace `YOUR-FRONTEND-URL` with your Vercel domain (we'll get this in the next section).

### 2.4 Deploy

Click **"Create Web Service"** and wait for deployment to complete.

**Note:** Render will provide a URL like: `https://stocksense-ai-backend.onrender.com`

Save this URL - you'll need it for the frontend!

### 2.5 Wait for Successful Deployment

Check the logs to ensure:
- ✅ Build completed successfully
- ✅ Server started on `0.0.0.0:PORT`
- ✅ No Python errors in logs

---

## Part 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub (recommended)

### 3.2 Import Project

1. Click **"Add New..."** → **"Project"**
2. Select your `stocksense-ai` GitHub repository
3. Vercel auto-detects Next.js (click **"Next.js"** if prompted)

### 3.3 Set Environment Variables

In Vercel dashboard, **Settings** → **Environment Variables**, add:

```
NEXT_PUBLIC_API_URL=https://stocksense-ai-backend.onrender.com
```

Use your Render backend URL from Part 2.4

### 3.4 Configure Build

Vercel auto-detects Next.js correctly, but verify:
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Node.js Version:** 20.x (default)

### 3.5 Deploy

Click **"Deploy"** and wait for:
- ✅ Build completed
- ✅ All checks passed
- ✅ Deployment to production

Vercel will provide a URL like: `https://stocksense-ai.vercel.app`

---

## Part 4: Update Backend with Frontend URL

### 4.1 Get Your Vercel URL

From Vercel dashboard, copy your frontend domain (e.g., `https://stocksense-ai.vercel.app`)

### 4.2 Update Render Environment Variables

1. Go to Render dashboard
2. Select your backend service
3. Click **Environment** → Edit `ALLOWED_ORIGINS`
4. Update to: `https://YOUR-FRONTEND-URL.vercel.app`
5. Deploy by manually triggering a redeploy or pushing a trivial code change

---

## Part 5: Testing

### 5.1 Test Frontend Loads

Visit: `https://stocksense-ai.vercel.app`

You should see:
- ✅ Homepage loads
- ✅ Navigation works
- ✅ Dashboard page accessible
- ✅ No console errors

### 5.2 Test PDF Analyzer

1. Go to `https://stocksense-ai.vercel.app/dashboard/pdf`
2. Upload a sample PDF
3. Should see: Loading spinner → Results display

**Success indicators:**
- ✅ File uploads without errors
- ✅ "Analyzing your PDF..." spinner appears
- ✅ Results display (summary, positives, risks, outlook)
- ✅ No "Backend server not running" error

### 5.3 Test Chart Analyzer

1. Go to `https://stocksense-ai.vercel.app/dashboard/chart`
2. Upload a stock chart image (PNG/JPG)
3. Should see: Preview → Loading → Pattern results

**Success indicators:**
- ✅ Image uploads without errors
- ✅ Image preview displays
- ✅ "Analyzing chart..." spinner appears
- ✅ Pattern results show (name, signal, confidence, description)
- ✅ Color-coded badges display

### 5.4 Test Backend API Directly

```bash
# Test health check
curl https://stocksense-ai-backend.onrender.com/health

# Test API docs
curl https://stocksense-ai-backend.onrender.com/docs
```

Both should return 200 OK.

---

## Part 6: Troubleshooting

### Issue: "Backend server not running" error

**Solution:**
1. Check Render dashboard - service should be running
2. Verify `NEXT_PUBLIC_API_URL` is set in Vercel
3. Verify `ALLOWED_ORIGINS` includes your Vercel domain in Render
4. Wait 60 seconds (Render cold start) and retry

### Issue: PDF/Chart analysis fails with 500 error

**Check:**
1. Backend logs in Render dashboard
2. Verify `OPENAI_API_KEY` is set correctly in Render Env
3. Check OpenAI account has credits/active subscription
4. Verify API key format: should start with `sk-`

### Issue: CORS errors in browser

**Solution:**
1. Check browser console for exact error
2. Verify `ALLOWED_ORIGINS` in Render matches your Vercel domain exactly
3. Redeploy backend after changing CORS settings

### Issue: Vercel says "Module not found"

**Solution:**
1. Verify `npm install` ran successfully
2. Check that all imports are correct
3. Redeploy from Vercel dashboard

---

## Part 7: Monitoring & Maintenance

### Monitor Backend Health

- **Render Dashboard:** View logs for errors
- **Health endpoint:** Visit `https://YOUR-BACKEND.onrender.com/health`
- **OpenAI costs:** Check your OpenAI account at platform.openai.com

### Monitor Frontend Health

- **Vercel Analytics:** Dashboard shows deployment health
- **Vercel Logs:** Check build and runtime logs
- **Browser DevTools:** Check for client-side errors

### Auto-Redeployment

- **Render:** Auto-redeploys on GitHub push (if enabled)
- **Vercel:** Auto-redeploys on GitHub push to main branch

---

## Part 8: Costs

### Estimated Monthly Costs

| Component | Provider | Cost |
|-----------|----------|------|
| Frontend | Vercel | **FREE** (free tier) |
| Backend | Render | **$7/month** (after free trial) |
| OpenAI API | OpenAI | **~$1-10/month** (~$0.01 per PDF analysis) |
| **Total** | | **~$8-17/month** |

### Cost Management Tips

- Monitor OpenAI usage at platform.openai.com
- Use GPT-3.5-turbo (cheaper than GPT-4)
- Set usage limits in OpenAI account settings

---

## Part 9: Production URLs

Once deployed, your URLs are:

```
Frontend: https://stocksense-ai.vercel.app
Backend API: https://stocksense-ai-backend.onrender.com
API Docs: https://stocksense-ai-backend.onrender.com/docs
Health Check: https://stocksense-ai-backend.onrender.com/health
```

---

## Next Steps

### Optional Enhancements

1. **Custom Domain:**
   - Vercel: Add custom domain in project settings
   - Render: Add custom domain in service settings

2. **Error Tracking:**
   - Add Sentry for production error monitoring

3. **Analytics:**
   - Add Google Analytics to Vercel frontend

4. **Database:**
   - Add PostgreSQL for storing analysis history (future)

5. **Authentication:**
   - Add auth0 or next-auth for user accounts (future)

---

## Support

If deployment fails:

1. **Check Render logs:** In Render dashboard → Logs tab
2. **Check Vercel logs:** In Vercel dashboard → Deployments → Logs
3. **Verify environment variables:**
   - `NEXT_PUBLIC_API_URL` in Vercel
   - `OPENAI_API_KEY` and `ALLOWED_ORIGINS` in Render
4. **Test manually:**
   - Visit backend health: `https://YOUR-BACKEND.onrender.com/health`
   - Check API docs: `https://YOUR-BACKEND.onrender.com/docs`

---

**Deployment Status:** 🟢 Ready for Production

All files are configured. You're ready to deploy!
