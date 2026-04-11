# ⚡ QUICK REFERENCE: Frontend Deployment to Vercel

## What's Ready
✓ Next.js frontend builds successfully
✓ All 11 pages compile without errors
✓ API integration with environment variables
✓ Vercel configuration complete
✓ TypeScript: No issues

## Deployment in 3 Steps

### Step 1: Get Backend URL (2 min)
```
Go to: https://dashboard.render.com
Click: stocksense-ai-backend
Copy: The service URL (format: https://stocksense-ai-backend.onrender.com)
```

### Step 2: Deploy Frontend to Vercel (2 min)
```
Go to: https://vercel.com/new
Choose: Import Git Repository
Select: ai-stock-analysis
Click: Deploy
```

### Step 3: Add Environment Variable (2 min)
```
In Vercel Dashboard:
  1. Click your new project
  2. Settings → Environment Variables
  3. Add:
     Name: NEXT_PUBLIC_API_URL
     Value: [Paste Render backend URL from Step 1]
     Environment: Production
  4. Save
  5. Go to Deployments → Redeploy latest
```

## Test Your App
```
1. Visit: https://YOUR-PROJECT.vercel.app/dashboard
2. Click: PDF Explainer
3. Upload a PDF → Should show analysis
4. Click: Chart Analyzer
5. Upload a chart → Should show pattern
```

## Environment Variables Reference

| Variable | Value | Where Set |
|----------|-------|-----------|
| `NEXT_PUBLIC_API_URL` | Your Render backend URL | Vercel Dashboard |

---

## Build Commands

```bash
# Local development
npm run dev

# Production build (tests locally)
npm run build

# Start production server locally
npm run start

# Linting
npm run lint
```

---

## Vercel URLs After Deployment

- Frontend: `https://YOUR-PROJECT.vercel.app`
- Dashboard: `https://YOUR-PROJECT.vercel.app/dashboard`
- PDF Tool: `https://YOUR-PROJECT.vercel.app/dashboard/pdf`
- Chart Tool: `https://YOUR-PROJECT.vercel.app/dashboard/chart`

---

## Troubleshooting

**"Backend not running" error?**
→ Check `NEXT_PUBLIC_API_URL` is set correctly in Vercel
→ Verify Render backend is running
→ Redeploy frontend after adding env var

**Build fails?**
→ Run `npm run build` locally to test
→ Check build logs in Vercel dashboard

**API not working?**
→ Environment variable must start with `NEXT_PUBLIC_`
→ Must redeploy after env changes
→ Clear browser cache
