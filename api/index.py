"""Vercel Serverless Function Entrypoint for TerraTrend."""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
TREND_DETECTIVE_DIR = os.path.join(BASE_DIR, "trend-detective")

# Ensure submodules are in sys.path
for p in [BACKEND_DIR, TREND_DETECTIVE_DIR, BASE_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Serverless environments only allow writing to /tmp
os.environ["MPLCONFIGDIR"] = "/tmp/.matplotlib_cache"
try:
    os.makedirs("/tmp/.matplotlib_cache", exist_ok=True)
except Exception:
    pass

from app.main import app
