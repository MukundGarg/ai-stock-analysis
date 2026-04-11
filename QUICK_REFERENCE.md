# 🚀 QUICK DEPLOYMENT REFERENCE CARD

Keep this handy while deploying!

---

## Before You Start

- [ ] GitHub account ready
- [ ] OpenAI API key: `sk-xxx...` (from platform.openai.com)
- [ ] Vercel account (free at vercel.com)
- [ ] Render account (free at render.com)

---

## STEP 1: Push to GitHub (2 min)

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai"
git init
git add .
git commit -m "Production-ready StockSense AI"
git remote add origin https://github.com/YOUR_USERNAME/stocksense-ai.git
git branch -M main
git push -u origin main
```

**After:** Code is on GitHub

---

## STEP 2: Deploy Backend - Render (5 min)

1. **Login:** https://render.com
2. **Click:** "New +" → "Web Service"
3. **Select:** Your GitHub repo
4. **Fill in:**
   - Name: `stocksense-ai-backend`
   - Runtime: `Python 3`
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Environment Variables:**
   - `OPENAI_API_KEY` = your actual key
   - `ALLOWED_ORIGINS` = `http://localhost:3000`

6. **Click:** "Create Web Service"
7. **Wait:** 3-5 minutes for deployment

**After:** Copy your Render URL (looks like: `https://stocksense-ai-backend.onrender.com`)

---

## STEP 3: Deploy Frontend - Vercel (5 min)

1. **Login:** https://vercel.com
2. **Click:** "Add New" → "Project"
3. **Select:** GitHub repo
4. **Next:** Framework auto-detection (should say Next.js)
5. **Settings → Environment Variables:**
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://stocksense-ai-backend.onrender.com` (your Render URL)

6. **Click:** "Deploy"
7. **Wait:** 2-3 minutes

**After:** Copy your Vercel URL (looks like: `https://stocksense-ai.vercel.app`)

---

## STEP 4: Update Backend CORS (2 min)

1. **Go:** Render dashboard
2. **Select:** `stocksense-ai-backend`
3. **Click:** Environment tab
4. **Edit:** `ALLOWED_ORIGINS`
5. **Change to:** `https://stocksense-ai.vercel.app` (your Vercel URL)
6. **Save:** Auto-redeploys

**After:** CORS updated for production

---

## STEP 5: Test Everything (5 min)

### Test 5A: Frontend Loads
```
Visit: https://YOUR-VERCEL-URL.vercel.app
Expected: Homepage with navigation
```

### Test 5B: PDF Analyzer
```
Go to: /dashboard/pdf
Upload: Any PDF file
Expected: Results appear (no "Backend not running" error)
```

### Test 5C: Chart Analyzer
```
Go to: /dashboard/chart
Upload: Stock chart image (PNG/JPG)
Expected: Pattern + Signal + Confidence displayed
```

### Test 5D: Backend Health
```
Visit: https://YOUR-RENDER-URL.onrender.com/health
Expected: {"status":"ok"}
```

### Test 5E: CORS Working
```
Try: PDF or Chart upload
Expected: No error in browser console (F12 → Console)
```

---

## ✅ Success Indicators

All of these should be TRUE:

| Check | Status |
|-------|--------|
| Frontend loads at Vercel URL | ✅ |
| Backend responds at health endpoint | ✅ |
| PDF analyzer returns results | ✅ |
| Chart analyzer returns patterns | ✅ |
| No "Backend server not running" errors | ✅ |
| No CORS errors in browser console | ✅ |

---

## 🔴 If Something Goes Wrong

### "Backend server not running"
```
1. Check Render dashboard → green status?
2. Verify NEXT_PUBLIC_API_URL in Vercel
3. Wait 60 seconds (cold start)
4. Retry
```

### CORS Errors
```
1. Check exact Vercel URL spelling
2. Update ALLOWED_ORIGINS in Render
3. Wait 2 minutes
4. Retry
```

### Build Failed
```
1. Check Vercel/Render logs
2. Ensure all files pushed to GitHub
3. Try manual redeploy
```

### OpenAI Analysis Fails
```
1. Check API key is set in Render
2. Verify key starts with "sk-"
3. Check OpenAI account has credits
4. Check Render logs
```

---

## 📱 URLs When Done

Save these URLs!

```
Frontend:    https://YOUR-APP-NAME.vercel.app
Backend API: https://YOUR-BACKEND-NAME.onrender.com
API Docs:    https://YOUR-BACKEND-NAME.onrender.com/docs
Health:      https://YOUR-BACKEND-NAME.onrender.com/health
```

---

## 💰 Costs

```
Vercel Frontend  $0
Render Backend   $7/month (after free trial)
OpenAI API       $2-10/month (based on usage)
───────────────────────────
TOTAL            $9-17/month
```

---

## 📞 Need More Help?

- **Quick summary:** [DEPLOY_NOW.md](./DEPLOY_NOW.md)
- **Detailed guide:** [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Environment vars:** [ENV_VARIABLES.md](./ENV_VARIABLES.md)
- **Full checklist:** [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)

---

## ⏱️ Timeline

| Step | Duration | Cumulative |
|------|----------|-----------|
| 1. Push to GitHub | 2 min | 2 min |
| 2. Deploy Backend | 5 min | 7 min |
| 3. Deploy Frontend | 5 min | 12 min |
| 4. Update CORS | 2 min | 14 min |
| 5. Test | 5 min | 19 min |
| | | **~20 min total** |

---

**You've got this! 🚀**
