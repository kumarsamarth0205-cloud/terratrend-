# TerraTrend Platform - Production Deployment Guide

This project is an integrated, production-ready platform combining:
1. **Frontend**: Vanilla HTML5/CSS/JavaScript with responsive dark-mode NASA UI
2. **Backend**: FastAPI web service integrating NASA POWER API
3. **Trend-Detective**: Mathematical & statistical data science engine (Mann-Kendall, Sen's Slope, Pettitt change point detection, 288-month Lucknow MERRA-2 ground-truth)

---

## 1. Instant Live Public Access (Available Right Now)

The platform is currently tunneled live to the public internet via Cloudflare Global Edge:

- **Public URL**: [https://shopping-pulling-links-fridge.trycloudflare.com](https://shopping-pulling-links-fridge.trycloudflare.com)
- **Interactive Swagger Docs**: [https://shopping-pulling-links-fridge.trycloudflare.com/docs](https://shopping-pulling-links-fridge.trycloudflare.com/docs)
- **API Health Endpoint**: [https://shopping-pulling-links-fridge.trycloudflare.com/api/health](https://shopping-pulling-links-fridge.trycloudflare.com/api/health)

---

## 2. Deploy to Render.com (1-Click Free Cloud Web Service)

Render provides free 24/7 hosting with automatic SSL and continuous deployment from GitHub.

### Step 1: Push to your GitHub account
```bash
# Create a new repository on https://github.com/new
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [https://dashboard.render.com](https://dashboard.render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository.
4. Render will automatically detect `render.yaml`:
   - **Environment**: Python 3.12
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**. Your app will be live at `https://<your-app>.onrender.com`.

---

## 3. Deploy to Railway.app

1. Go to [https://railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select this repository.
4. Railway will automatically detect `railway.json` and deploy using the root `Dockerfile` or `Procfile`.
5. Under Settings -> Networking, click **Generate Domain** to get a public URL like `https://terratrend.up.railway.app`.

---

## 4. Deploy with Docker

You can run the production container anywhere Docker is installed (AWS, GCP, DigitalOcean, Azure):

```bash
# Build production image
docker build -t terratrend:latest .

# Run container on port 8000
docker run -d --name terratrend-app -p 8000:8000 terratrend:latest

# Verify health
curl http://localhost:8000/api/health
```

---

## 5. Local Production Execution

To run locally anytime on your machine:

```bash
# Windows
start.bat
# or
python run_all.py
```

- Web Interface: [http://localhost:3000](http://localhost:3000) or [http://localhost:8000](http://localhost:8000)
- Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
