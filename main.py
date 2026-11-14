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

# Ensure backend and trend-detective are first in sys.path
for p in [BACKEND_DIR, TREND_DETECTIVE_DIR, BASE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Configure writable cache directory for Matplotlib (supports serverless /tmp)
_mpl_dir = os.environ.get("MPLCONFIGDIR") or (
    "/tmp/.matplotlib_cache" if os.path.exists("/tmp") else os.path.join(BASE_DIR, ".matplotlib_cache")
)
os.environ["MPLCONFIGDIR"] = _mpl_dir
try:
    os.makedirs(_mpl_dir, exist_ok=True)
except Exception:
    pass

# Import the core FastAPI app from backend/app
from app.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
