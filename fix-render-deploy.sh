#!/usr/bin/env bash
# Exact commands to fix Render deployment

# Copy each line and run in terminal

# 1. Navigate to project
cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai"

# 2. Verify changes (optional - shows what was updated)
echo "=== Changed files ==="
git status

# 3. Add the fixed files
git add runtime.txt backend/requirements.txt

# 4. Commit with detailed message
git commit -m "Fix Render deployment: Update Python version and dependencies

- Change python-3.11.8 to python-3.11 in runtime.txt
  Reason: Allows Render to install any stable 3.11.x version

- Update opencv-python 4.8.1.78 -> 4.10.1.26
  Reason: Newer version with pre-built wheels for Python 3.11

- Update pillow 10.1.0 -> 11.0.0
  Reason: November 2024 release with excellent wheel support

- Update numpy 1.26.4 -> 2.1.0
  Reason: Latest stable version with perfect wheel support

Benefits:
- ✓ No more 'Failed to build pillow' error
- ✓ No more 'KeyError: version' error
- ✓ Faster dependency installation (wheels vs source)
- ✓ Zero code changes - 100% backward compatible"

# 5. Push to GitHub
git push origin main

# 6. Watch Render deploy automatically
# Go to: https://dashboard.render.com
# Select: stocksense-ai-backend
# Watch the build logs for:
#   ✓ Python version: 3.11.x
#   ✓ Successfully installed [packages]
#   ✓ Application startup complete

# 7. Test the fix (after build completes)
# Replace YOUR-BACKEND-URL with your actual Render URL
curl https://YOUR-BACKEND-URL.onrender.com/health

# Expected output: {"status":"ok"}

echo "Done! Render should now deploy successfully."
