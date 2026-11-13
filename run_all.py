"""TerraTrend Integrated Master Launcher.
Launches the connected NASA Space Apps 2026 platform:
1. Backend (FastAPI + NASA POWER) with Trend-Detective data science engine on http://localhost:8000
2. Frontend (HTML5/CSS/JS) on http://localhost:3000 & directly on http://localhost:8000
"""
import os
import sys
import time
import subprocess

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

def main():
    print("=" * 70)
    print(">>> TERRATREND & EARTH SYSTEM TREND DETECTIVE - LAUNCHER")
    print("=" * 70)
    print(f"Base Directory: {BASE_DIR}")
    print("Connecting all 3 repositories:")
    print("  1. Frontend:        TerraTrend Web Application")
    print("  2. Backend:         FastAPI NASA POWER Service")
    print("  3. Trend-Detective: Data Science & Statistical Engine")
    print("-" * 70)

    # Start FastAPI Backend (Port 8000)
    print("[*] Starting Unified Backend & Engine on http://localhost:8000 ...")
    backend_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    backend_proc = subprocess.Popen(backend_cmd, cwd=BACKEND_DIR)

    # Start Dedicated Frontend Static Server (Port 3000)
    print("[*] Starting Dedicated Frontend Server on http://localhost:3000 ...")
    frontend_cmd = [sys.executable, "-m", "http.server", "3000", "--directory", FRONTEND_DIR]
    frontend_proc = subprocess.Popen(frontend_cmd, cwd=FRONTEND_DIR)

    time.sleep(3)
    print("\n[OK] All services are RUNNING and CONNECTED!")
    print("-" * 70)
    print("ACCESS YOUR APPLICATION:")
    print("  -> Option A (Port 3000):  http://localhost:3000")
    print("  -> Option B (Port 8000):  http://localhost:8000")
    print("  -> Swagger API Docs:      http://localhost:8000/docs")
    print("  -> System Health Check:   http://localhost:8000/api/health")
    print("-" * 70)
    print("Press Ctrl+C to stop all servers.")

    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping all services...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
