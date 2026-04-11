# ⚡ Quick Fix - Copy & Paste Commands

Your Render build will now succeed. Just run these 3 commands:

---

## Step 1: Commit (1 minute)

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai"
git add backend/requirements.txt
git commit -m "Fix opencv-python version: use valid 4.8.1.78 headless version

- Replace non-existent opencv-python==4.10.1.26 with real version
- Use opencv-python-headless==4.8.1.78 (better for server)
- Update numpy==1.24.3 for compatibility
- All packages now have wheels for Python 3.11"
```

---

## Step 2: Push (1 minute)

```bash
git push origin main
```

---

## Step 3: Redeploy on Render (5 minutes wait)

Go to https://dashboard.render.com:

1. Select `stocksense-ai-backend` service
2. Click "Deploy" or let auto-deploy trigger
3. Watch logs for:
   - ✓ "Successfully installed opencv-python-headless==4.8.1.78"
   - ✓ "Successfully installed numpy==1.24.3"
   - ✓ "Application startup complete"
   - ✓ "Uvicorn running on 0.0.0.0:PORT"

---

## That's It! ✓

Build should succeed now. No more "No matching distribution found" errors.

---

## Key Changes

| Package | Old | New | Why |
|---------|-----|-----|-----|
| opencv | opencv-python==4.10.1.26 (fake) | opencv-python-headless==4.8.1.78 (real) | Real version, headless for servers |
| numpy | 2.1.0 | 1.24.3 | Better compatibility |

---

See [FIX_ROUND2.md](./FIX_ROUND2.md) for full technical details.
