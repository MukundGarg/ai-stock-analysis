# 🔧 FRONTEND-BACKEND CONNECTION FIX

## Problems Identified & Fixed

### Problem 1: CORS Blocking ❌
**Issue**: Backend CORS only allowed localhost, blocking Vercel frontend URL
**Status**: ✅ FIXED
- Added `https://ai-stock-analysis-orpin.vercel.app` to backend CORS
- Changes committed to GitHub

### Problem 2: Missing Environment Variable ❌
**Issue**: `NEXT_PUBLIC_API_URL` not set in Vercel, frontend falls back to localhost
**Status**: 🔧 NEEDS YOUR ACTION
- Frontend code is correct (uses environment variable with localhost fallback)
- Variable needs to be added in Vercel Dashboard

---

## 🚀 HOW TO FIX - 3 MINUTES

### Step 1: Redeploy Backend (1 min)

Go to: **https://dashboard.render.com**

1. Click `stocksense-ai-backend`
2. Click **"Deploy"** button
3. Wait for build to complete

This applies the CORS fix.

### Step 2: Set Environment Variable in Vercel (2 min)

Go to: **https://vercel.com**

1. Click your project: `ai-stock-analysis-orpin`
2. Go to **Settings** → **Environment Variables**
3. Click **"Add New Environment Variable"**
4. Fill in exactly:
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: https://stocksense-ai-backend-7p8f.onrender.com
   Environment: Production
   ```
5. Click **"Save"**
6. You'll see a notification: "Added 1 environment variable"

### Step 3: Redeploy Frontend (1 min)

1. Go to **Deployments** tab
2. Find the most recent deployment
3. Click the **"Redeploy"** button (three dots menu → Redeploy)
4. Wait 2-3 minutes for redeployment

---

## ✅ How to Verify It Works

After redeployment completes:

### Test in Browser

1. Visit: **https://ai-stock-analysis-orpin.vercel.app/dashboard/pdf**
2. Open **Developer Tools** (F12)
3. Go to **Console** tab
4. You should see:
   ```
   [PDF Analyzer] Using API URL: https://stocksense-ai-backend-7p8f.onrender.com
   ```

### Upload a Test PDF

1. Click "Choose File" or drag a PDF
2. Wait 10-30 seconds
3. Should show analysis (not an error)

### Check Network Tab

In Developer Tools:
1. Go to **Network** tab
2. Upload a PDF
3. Watch for request to:
   ```
   https://stocksense-ai-backend-7p8f.onrender.com/analyze-pdf
   ```
4. Status should be **200** (success), not 403/CORS error

---

## 🔍 Troubleshooting

### Still Getting "Backend server not running" Error

**Issue 1: Environment Variable Not Set**
- ❌ Variable missing from Vercel Dashboard
- ✅ Fix: Follow Step 2 above, make sure to **Save**

**Issue 2: Old Deployment Still Running**
- ❌ Forgot to redeploy
- ✅ Fix: Go to Deployments → Redeploy latest

**Issue 3: Environment Variable Not Applied**
- ❌ Variable added but old deployment still active
- ✅ Fix: Redeploy after adding variable (must wait for new deployment to complete)

### CORS Error in Browser Console

**Message**: `Access to XMLHttpRequest at 'https://...' from origin 'https://...' has been blocked by CORS policy`

- ❌ Old CORS config still active on backend
- ✅ Fix: Redeploy backend on Render (wait for build to complete)

### Check if Backend is Running

```bash
curl https://stocksense-ai-backend-7p8f.onrender.com/health
```

Should return:
```json
{"status":"healthy","service":"StockSense AI Backend","version":"1.0.0"}
```

---

## 📋 Complete Checklist

- [ ] Backend redeployed on Render
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel (Settings → Environment Variables)
- [ ] Frontend redeployed after adding env var
- [ ] Browser console shows: `[PDF Analyzer] Using API URL: https://stocksense-ai-backend-7p8f.onrender.com`
- [ ] Network tab shows requests to actual backend URL (not localhost)
- [ ] PDF upload succeeds with analysis results
- [ ] Chart upload succeeds with pattern detection

---

## 🔐 Security Reminders

**IMPORTANT: Rotate Your OpenAI API Key**

You exposed your API key earlier. Please:
1. Go to **https://platform.openai.com/account/api-keys**
2. Delete the exposed key
3. Create a new key
4. Add to Render: **Settings** → **Environment Variables** → `OPENAI_API_KEY`

---

## 💡 How It Works Now

```
Browser (https://ai-stock-analysis-orpin.vercel.app)
    ↓
JavaScript reads: process.env.NEXT_PUBLIC_API_URL
    ↓
    → If set in Vercel: https://stocksense-ai-backend-7p8f.onrender.com ✅
    → If NOT set: http://localhost:8000 ❌ (fails in production)
    ↓
Fetch to Backend API
    ↓
Backend checks CORS
    ↓
    → If origin in ALLOWED_ORIGINS: ✅ Request allowed
    → If not: ❌ CORS error
```

Current setup:
- ✅ Frontend: Code uses environment variable correctly
- ✅ Backend: CORS now accepts Vercel URL
- 🔧 Missing: Environment variable set in Vercel Dashboard

---

## 📊 Summary of Changes

| Component | Issue | Status |
|-----------|-------|--------|
| Frontend Code | Uses env var (correct) | ✅ No changes needed |
| Backend CORS | Blocked Vercel URL | ✅ Fixed (committed) |
| Vercel Env Var | Not set | 🔧 **You need to set this** |
| Render Backend | Working | ✅ Ready |

---

## ⏭️ Next Steps

1. **Redeploy backend** on Render (1 min)
2. **Add environment variable** in Vercel (2 min)
3. **Redeploy frontend** on Vercel (2 min)
4. **Test** by uploading PDF (1 min)

**Total: 6 minutes to fully working application!**

---

See **DEPLOYMENT_ACTION_PLAN.md** for complete deployment steps if needed.
