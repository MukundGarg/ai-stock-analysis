# ✅ Deployment Checklist

Use this checklist to ensure your production deployment is successful.

---

## Pre-Deployment Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub main branch
- [ ] All files committed (no uncommitted changes)
- [ ] Vercel account created
- [ ] Render account created
- [ ] OpenAI API key obtained and ready
- [ ] Frontend code updated with environment variables
- [ ] Backend code updated with dynamic CORS

---

## Backend Deployment (Render)

### Setup
- [ ] Create new Web Service in Render
- [ ] Connect GitHub repository
- [ ] Set service name: `stocksense-ai-backend`
- [ ] Set runtime: Python 3
- [ ] Verify build command: `pip install -r backend/requirements.txt`
- [ ] Verify start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Environment Variables
- [ ] Add `OPENAI_API_KEY` (your actual key from platform.openai.com)
- [ ] Add `ALLOWED_ORIGINS` (temporary: `http://localhost:3000`)
- [ ] Deploy

### After Deployment
- [ ] Deployment completes successfully (green checkmark)
- [ ] Logs show "Application startup complete"
- [ ] No Python errors in logs
- [ ] Backend URL: `https://YOUR-SERVICE-NAME.onrender.com`
- [ ] Save backend URL for frontend setup

---

## Frontend Deployment (Vercel)

### Setup
- [ ] Create new project in Vercel
- [ ] Select GitHub repository `stocksense-ai`
- [ ] Vercel auto-detects Next.js framework
- [ ] Framework preset set to Next.js
- [ ] Build command verified: `npm run build`
- [ ] Output directory verified: `.next`

### Environment Variables
- [ ] Add `NEXT_PUBLIC_API_URL` = `https://YOUR-BACKEND-NAME.onrender.com`
- [ ] Deploy

### After Deployment
- [ ] Deployment completes successfully (green checkmark)
- [ ] All checks pass
- [ ] Preview works (can see homepage)
- [ ] Frontend URL: `https://YOUR-PROJECT-NAME.vercel.app`
- [ ] Save frontend URL

---

## Update Backend CORS

### After Frontend Deployed
- [ ] Copy exact frontend URL from Vercel
- [ ] Go to Render dashboard → Your backend service
- [ ] Click "Environment" tab
- [ ] Edit `ALLOWED_ORIGINS` variable
- [ ] Update to: `https://YOUR-FRONTEND-URL.vercel.app`
- [ ] Save changes
- [ ] Manual redeploy or push a code change to trigger redeploy
- [ ] Verify deployment completes

---

## Testing Phase

### Test Frontend Loads
- [ ] Visit `https://YOUR-FRONTEND-URL.vercel.app`
- [ ] Page loads completely (no blank page)
- [ ] Navigation bar visible
- [ ] No console errors (press F12 to check)

### Test PDF Analyzer Section
- [ ] Navigate to `/dashboard/pdf`
- [ ] Page loads (upload area visible)
- [ ] Upload a sample PDF file
- [ ] See "Analyzing your PDF..." spinner
- [ ] Results appear after analysis
- [ ] Can upload another PDF

### Test Chart Analyzer Section
- [ ] Navigate to `/dashboard/chart`
- [ ] Page loads (upload area visible)
- [ ] Upload a sample chart image (PNG or JPG)
- [ ] See image preview
- [ ] See "Analyzing chart..." spinner
- [ ] Pattern results appear
- [ ] Color-coded badges show (Bullish/Bearish/Neutral)
- [ ] Can upload another chart

### Test Backend Directly
- [ ] Visit `https://YOUR-BACKEND-URL/health` → should return 200
- [ ] Visit `https://YOUR-BACKEND-URL/docs` → API documentation loads

---

## Troubleshooting

### Frontend doesn't load
- [ ] Check Vercel deployment status (should be green)
- [ ] Check browser console for errors (F12)
- [ ] Verify frontend URL is correct
- [ ] Hard refresh page (Cmd+Shift+R or Ctrl+Shift+R)

### "Backend server not running" error
- [ ] Check backend is deployed on Render
- [ ] Check `NEXT_PUBLIC_API_URL` matches backend URL exactly
- [ ] Check Render backend is running (green status)
- [ ] Wait 60 seconds (cold startup) and retry

### PDF/Chart analysis returns error
- [ ] Check `OPENAI_API_KEY` is set in Render
- [ ] Check OpenAI account has active credits
- [ ] Check Render logs for error messages
- [ ] Verify API key format (should start with sk-)

### CORS errors (red X in browser)
- [ ] Check `ALLOWED_ORIGINS` in Render includes frontend URL
- [ ] Wait 2 minutes after updating CORS
- [ ] Test again
- [ ] Check exact URL match (https vs http, www, etc.)

---

## Post-Deployment

### Monitor
- [ ] Check Render logs daily for errors
- [ ] Check Vercel analytics
- [ ] Monitor OpenAI usage at platform.openai.com
- [ ] Set up low-credit alerts in OpenAI

### Maintain
- [ ] Keep dependencies updated (monthly)
- [ ] Update OpenAI API key if compromised
- [ ] Review and optimize costs
- [ ] Plan for scaling (if needed)

---

## Success Indicators ✅

All of these should be true:

- ✅ Frontend loads at `https://YOUR-FRONTEND-URL.vercel.app`
- ✅ Backend API responds at `https://YOUR-BACKEND-URL/health`
- ✅ PDF analyzer works (analyze, get results)
- ✅ Chart analyzer works (upload, see pattern detection)
- ✅ No console errors in browser
- ✅ No errors in Render backend logs
- ✅ CORS working (no cross-origin errors)
- ✅ OpenAI API calls succeed

---

## Deployment Complete! 🎉

When all checkboxes above are ✅, your application is successfully deployed to production.

**Public URLs:**
- Frontend: `[SAVE YOUR URL]`
- Backend API: `[SAVE YOUR URL]`
- API Docs: `[SAVE YOUR URL]/docs`

Share the frontend URL with others to use your application!
