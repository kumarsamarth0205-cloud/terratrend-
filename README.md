# 🛰️ TerraTrend & Earth System Trend Detective (Integrated Full-Stack)
> **NASA Space Apps Challenge 2026** — Unified Platform

This workspace connects all three repositories into a single cohesive full-stack Earth science analytics platform:

1. **Frontend (`frontend/`)**: [firestrom-frontend](https://github.com/PranavUI3/firestrom-frontend)
   - Interactive scientific web interface (Dashboard, Trend Detective, Global Map, Regional Comparison, Variables Catalog, Demos).
2. **Backend (`backend/`)**: [firestorm-backend](https://github.com/vanshmodanwal01/firestorm-backend)
   - FastAPI web service connected to NASA POWER API and REST endpoints.
3. **Data Science Module (`trend-detective/`)**: [trend-detective](https://github.com/rishabhsinghchauhan667/trend-detective)
   - Statistical engine: Seasonal climatology removal, Mann-Kendall with Hamed-Rao / AR(1) autocorrelation correction, Sen's slope with 95% confidence intervals, and real Giovanni validation data.

---

## 🔗 Architecture & Connection Overview

```
 ┌─────────────────────────────────────────────────────────────┐
 │               TerraTrend Frontend (HTML5/CSS/JS)            │
 │     http://localhost:3000   OR   http://localhost:8000      │
 └──────────────────────────────┬──────────────────────────────┘
                                │ JSON API Calls
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │                FastAPI Backend (app/main.py)                │
 │       Unified API Router: /api/analyze, /api/variables      │
 └──────────────┬──────────────────────────────┬───────────────┘
                │                              │
                ▼                              ▼
 ┌──────────────────────────────┐ ┌────────────────────────────┐
 │ NASA POWER Provider (Live)   │ │ Trend-Detective Engine     │
 │ Meteorological & Solar Data  │ │ Mann-Kendall + Sen's Slope │
 │ MERRA-2, CERES, GEWEX        │ │ Giovanni Real Datasets     │
 └──────────────────────────────┘ └────────────────────────────┘
```

---

## 🚀 Running the Project

Both servers are automatically started. You can access the application at:

- **Web Application:** [http://localhost:3000](http://localhost:3000) or [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Health Check:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

### To start manually anytime:
Double-click `start.bat` or run:
```powershell
python run_all.py
```
