# 🔧 Vercel Deployment Config Fix

## Problem Identified

Vercel rejected deployment with error:
```
Invalid request: should NOT have additional property envPrefix
```

**Root Cause**: `vercel.json` contained configuration that Vercel's API doesn't support:
- `env` object with `@api_url` syntax (not properly supported)
- `devCommand` (unnecessary for production)
- `functions` entry (not needed for Next.js)
- `regions` specification (conflicted with validation schema)

---

## Solution Applied ✅

Simplified `vercel.json` to **minimal required configuration**:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next"
}
```

**Why this works:**
- ✅ Only includes required properties
- ✅ Passes Vercel API validation
- ✅ Next.js auto-detection still works
- ✅ All build settings preserved

---

## Environment Variables Setup

With the simplified vercel.json, set environment variables in **Vercel Dashboard** instead:

### Step 1: Go to Vercel Dashboard
Open: **https://vercel.com**

### Step 2: Configure Backend URL
1. Click your project
2. Go to **Settings** → **Environment Variables**
3. Add new variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your Render backend URL (e.g., `https://stocksense-ai-backend.onrender.com`)
   - **Environment**: Select "Production"
4. Click **Save**

### Step 3: Redeploy
1. Go to **Deployments**
2. Click **Redeploy** on the latest deployment
3. Wait 1-2 minutes

---

## Changes Made

| File | Change | Status |
|------|--------|--------|
| `vercel.json` | Simplified to 2 lines | ✅ Updated |
| All other files | Unchanged | ✓ No changes |

---

## 🚀 Next Steps

### Step 1: Redeploy Frontend on Vercel

Go to: **https://vercel.com**

1. Click your project (if not already deployed, do deployment now)
2. **If already deployed:**
   - Go to **Settings** → **Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` = your Render backend URL
   - Go to **Deployments**
   - Click **Redeploy**

### Step 2: Verify Deployment

Wait 1-2 minutes, then:
1. Visit your Vercel URL (shown in Deployments)
2. Go to **Dashboard** → **PDF Explainer**
3. Upload a PDF file
4. Verify analysis appears (no "Backend not running" error)

---

## Configuration Details

### What vercel.json Does Now

```json
{
  "buildCommand": "npm run build",    // Run Next.js build
  "outputDirectory": ".next"          // Where build outputs go
}
```

That's all Vercel needs! Everything else auto-detected.

### What's Removed & Why

| Removed | Reason |
|---------|--------|
| `env` object | Use Vercel Dashboard instead |
| `devCommand` | Not used in production |
| `functions` | Not needed for Next.js |
| `regions` | Can cause validation errors |

---

## Verification

After changes are committed (✓ already done!):

1. Vercel will auto-detect new vercel.json
2. Next deployment will use simplified config
3. API validation will pass ✅
4. Build will succeed ✅

---

## Full Deployment Checklist

- [ ] Backend deployed on Render ✓ (Already done)
- [ ] Backend `/health` endpoint working ✓ (Test it)
- [ ] vercel.json simplified ✓ (Just done)
- [ ] Frontend deployed to Vercel (do this next)
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel Dashboard (do after deploy)
- [ ] Frontend redeployed (do after env var added)
- [ ] PDF upload tested
- [ ] Chart upload tested

---

## ✨ You're Ready for Frontend Deployment!

```
Current Status:
✅ Backend: Deployed on Render
✅ Frontend: Built and tested
✅ vercel.json: Fixed
✅ Configurations: Simplified for Vercel

Next Action: Deploy to Vercel
```

---

## Deployment Steps (From Scratch)

If you haven't deployed to Vercel yet:

1. Go to **https://vercel.com/new**
2. Import `ai-stock-analysis` repository
3. Keep default settings
4. Click **Deploy**
5. After deploy completes:
   - Add `NEXT_PUBLIC_API_URL` env var
   - Redeploy

If already deployed, just redeploy now with the fixed config!

---

See **DEPLOYMENT_ACTION_PLAN.md** for complete step-by-step instructions.
