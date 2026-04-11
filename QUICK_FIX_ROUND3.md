# ⚡ QUICK FIX - COPY & PASTE (Round 3)

## The Problem
Render uses Python 3.14.3, and numpy==1.24.3 has no wheels for Python 3.14, so it tried to compile from source but failed.

## The Solution
Use numpy 2.0+ which has pre-built wheels for Python 3.14.

---

## 3 Commands - 5 Minutes

### Command 1: Commit (1 min)

```bash
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai"
git add runtime.txt backend/requirements.txt
git commit -m "Fix Render build: Use numpy wheels for Python 3.14

- Change numpy==1.24.3 to >=2.0.0,<3.0.0
  NumPy 2.0+ has pre-built wheels for Python 3.14, no compilation needed

- Change pillow==10.1.0 to >=10.0.0
  Allow pip to choose compatible version

- Ensure runtime.txt specifies python-3.11
  Future builds will use Python 3.11

This prevents the setuptools.build_meta error."
```

### Command 2: Push (1 min)

```bash
git push origin main
```

### Command 3: Redeploy (5 min wait)

Go to: https://dashboard.render.com
- Select: stocksense-ai-backend
- Click: Deploy

Watch for:
```
✓ Downloading numpy-2.X.X...cp311...whl (wheel, not source!)
✓ Successfully installed [all packages]
✓ Application startup complete
✓ Build succeeded ✓
```

---

## What Changed

| File | Change |
|------|--------|
| `backend/requirements.txt` | numpy 1.24.3 → >=2.0.0,<3.0.0 |
| `backend/requirements.txt` | pillow 10.1.0 → >=10.0.0 |
| `runtime.txt` | python-3.11 (verified) |

---

## Why It Works

- numpy 2.0+ = has wheels for Python 3.14
- wheels = no source compilation needed
- no compilation = no setuptools error
- = build succeeds ✓

---

That's it! Run the 3 commands and you're done. ✅
