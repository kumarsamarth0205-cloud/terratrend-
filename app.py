"""TerraTrend Platform - Unified Production ASGI Application.
Mounts:
  - FastAPI NASA POWER & Trend-Detective API at /api and /api/v1
  - Swagger Documentation at /docs & /redoc
  - Static Frontend Web App at / and /{page}.html
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
TREND_DETECTIVE_DIR = os.path.join(BASE_DIR, "trend-detective")

# Ensure all submodules are available in sys.path
for path in [BASE_DIR, BACKEND_DIR, TREND_DETECTIVE_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Configure writable cache directory for Matplotlib
os.environ["MPLCONFIGDIR"] = os.path.join(BASE_DIR, ".matplotlib_cache")
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

# Import the core FastAPI app from backend
from backend.app.main import app as application

# Expose app for Uvicorn / Gunicorn
app = application

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
