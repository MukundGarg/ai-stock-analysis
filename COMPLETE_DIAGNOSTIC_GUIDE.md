# 🔍 COMPLETE DIAGNOSTIC & SETUP GUIDE

## Critical Issue Found ❌

The `vercel.json` file had **invalid environment variable syntax** that PREVENTED variables from being set:

```json
// WRONG - This syntax doesn't work in Vercel
"env": {
  "NEXT_PUBLIC_API_URL": "@api_url"
}
```

This has been **FIXED** and removed. Now you must set environment variables in the **Vercel Dashboard** (not in config files).

---

## What Needs Your Action

I've fixed the code. Now you need to:

### 1️⃣ Verify Backend is Running
✅ Can you confirm your backend is deployed on Render and the service says "Live"?

```bash
# Test backend health:
curl https://stocksense-ai-backend-7p8f.onrender.com/health
```

Should return:
```json
{"status":"healthy","service":"StockSense AI Backend","version":"1.0.0"}
```

### 2️⃣ Set Environment Variable in Vercel (REQUIRED)

Go to: **https://vercel.com/dashboard**

1. Click your project: `ai-stock-analysis-2vdxd4jek...`
2. Go to **Settings** tab
3. Click **Environment Variables** (left sidebar)
4. Click **"Add New Environment Variable"**
5. Fill in exactly:
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: https://stocksense-ai-backend-7p8f.onrender.com
   Environment: Production
   ```
6. Click **"Save"**
7. Go back to **Deployments** tab
8. Click **"Redeploy"** on latest deployment

**Wait for redeployment to complete!**

### 3️⃣ Test with Browser Console

After redeployment completes:

1. Visit: `https://ai-stock-analysis-2vdxd4jek.../dashboard/pdf`
2. Open **Developer Tools** (F12)
3. Click **Console** tab
4. Upload a PDF
5. **You should see in console:**
   ```
   [PDF] API URL: https://stocksense-ai-backend-7p8f.onrender.com
   [PDF] Uploading file: your-file.pdf
   [PDF] Response status: 200
   ```

If you see a different API URL (like `http://localhost:8000`), the environment variable is NOT set.

---

## What I Fixed in Code

### Fix #1: vercel.json
❌ **Before:**
```json
{
  "env": {
    "NEXT_PUBLIC_API_URL": "@api_url"
  }
}
```

✅ **After:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next"
}
```

### Fix #2: Frontend Debugging
Added console logs to both PDF and Chart analyzers so you can see:
- What API URL is being used
- If the request reaches the backend
- What HTTP status is returned
- Any errors that occur

### Fix #3: Backend
Already fixed in previous commits:
- Simplified CORS configuration
- Uses regex pattern to accept all vercel.app domains
- Middleware always active

---

## Verification Checklist

Please verify each of these and report back:

- [ ] Backend health check returns 200 OK
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel Dashboard
- [ ] Frontend redeployed after adding env var
- [ ] Browser console shows correct API URL (not localhost)
- [ ] Browser console shows response status 200
- [ ] No errors printing to console
- [ ] PDF upload completes instead of failing

---

## Testing Procedure

### Step 1: Verify Backend Running (1 min)
```bash
curl https://stocksense-ai-backend-7p8f.onrender.com/health
# Should return 200 with JSON response
```

### Step 2: Set Env Var in Vercel (2 min)
- Go to Vercel Settings → Environment Variables
- Add `NEXT_PUBLIC_API_URL` with your backend URL
- **Save**

### Step 3: Redeploy Frontend (3 min)
- Go to Deployments
- Click Redeploy
- Wait for "Ready" status

### Step 4: Test Upload (2 min)
1. Open frontend in browser
2. Open DevTools (F12)
3. Go to Console tab
4. Upload a PDF
5. Watch console for log messages

---

## Expected Console Output (Success)

```
[PDF] API URL: https://stocksense-ai-backend-7p8f.onrender.com
[PDF] Uploading file: my-document.pdf
[PDF] Response status: 200
(PDF analysis completes and displays results)
```

---

## Expected Console Output (Failure - Missing Env Var)

```
[PDF] API URL: http://localhost:8000  ← ❌ Wrong URL!
[PDF] Uploading file: my-document.pdf
[PDF] Error: Failed to fetch
```

If you see `http://localhost:8000`, the environment variable is NOT set.

---

## I Need Your Help With

Please run through the steps above and tell me:

1. **Backend health check:** Does it return 200?
2. **Vercel environment variable:** Is it set and saved?
3. **Console output:** What API URL shows in the console?
4. **Error details:** What does the error message show?

Once you provide this info, I can debug the exact issue.

---

## Files That Changed

✅ `vercel.json` - Fixed invalid env var config
✅ `app/dashboard/pdf/page.tsx` - Added debugging logs
✅ `app/dashboard/chart/page.tsx` - Added debugging logs
✅ `backend/main.py` - CORS already fixed
✅ `app.py` - Startup already fixed

All changes committed to GitHub.

---

## What Happens Next

Once you complete the steps above:

1. **If backend health check succeeds:** Backend is running fine
2. **If env var is set correctly:** Frontend will use correct URL
3. **If console shows correct API URL:** Environment variable is working
4. **If status is 200:** CORS is working and PDF will analyze
5. **If status is 403:** CORS needs more debugging
6. **If status is something else:** Backend returned an error

---

## Questions to Ask Yourself

✅ Is `NEXT_PUBLIC_API_URL` set in Vercel Dashboard?
✅ Did you click "Save" after adding the env var?
✅ Did you redeploy the frontend after adding the env var?
✅ Is the frontend showing the CORRECT API URL in console?
✅ Is the backend returning 200 status?
✅ Does the backend health endpoint respond?

---

## Next Steps

1. **Complete the verification checklist above**
2. **Tell me:**
   - Backend health check result
   - What API URL shows in console
   - What error you see (if any)
   - What status code is returned

Then I can provide specific fixes!

---

See `CORS_COMPLETE_FIX.md` and `DEPLOYMENT_ACTION_PLAN.md` for additional reference.
