"""
Entry point for Render deployment.
This script adds the backend directory to the path and starts the FastAPI app.
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path so we can import main
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Now we can import and run the app
from main import app

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
