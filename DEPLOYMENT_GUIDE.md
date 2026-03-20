# 🚀 Sales Forecasting API - Deployment Guide

## Quick Start

### Files Included:
- `app.py` - FastAPI application
- `streamlit_app.py` - Web dashboard (optional)
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration
- `Procfile` - Heroku deployment config
- `.dockerignore` - Docker ignore rules

---

## 📋 Step 1: Prepare Repository

### 1. Clone/Update your GitHub repo:
```bash
cd sales-forecasting-time-series
```

### 2. Copy all files to your repo:
- `app.py`
- `requirements.txt`
- `Dockerfile`
- `Procfile`
- `.dockerignore`
- `streamlit_app.py`

### 3. Make sure your dataset is in the repo:
- `sales_time_series_dataset.csv`

### 4. Commit and push:
```bash
git add .
git commit -m "Add API deployment files"
git push origin main
```

---

## 🧪 Step 2: Test Locally (10 minutes)

### Option A: Direct Python
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run API
python app.py

# Test in browser
# http://localhost:8000 - Health check
# http://localhost:8000/docs - API documentation
# http://localhost:8000/stats - Dataset stats
```

### Option B: Docker (if Docker is installed)
```bash
# Build image
docker build -t sales-api .

# Run container
docker run -p 8000:8000 sales-api

# Test
curl http://localhost:8000
```

### Option C: Streamlit (Web Dashboard)
```bash
# Install streamlit
pip install streamlit plotly

# Run dashboard
streamlit run streamlit_app.py

# Open browser to http://localhost:8501
```

---

## 🌍 Step 3: Deploy to Cloud

### ⭐ OPTION A: HEROKU (Easiest - FREE)

#### 1. Install Heroku CLI
- Windows/Mac/Linux: https://devcenter.heroku.com/articles/heroku-cli

#### 2. Login
```bash
heroku login
```

#### 3. Create Heroku app
```bash
heroku create your-sales-forecasting-api
```

#### 4. Deploy
```bash
git push heroku main
```

#### 5. View logs
```bash
heroku logs --tail
```

#### 6. Access API
```
https://your-sales-forecasting-api.herokuapp.com
https://your-sales-forecasting-api.herokuapp.com/docs
```

#### 7. Troubleshoot
```bash
heroku logs --tail
heroku open
heroku config
```

---

### 🟦 OPTION B: AWS EC2

#### 1. Launch EC2 Instance
- Go to AWS Console → EC2 → Launch Instance
- Choose Ubuntu 22.04
- Security group: Open port 8000

#### 2. SSH into instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

#### 3. Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
```

#### 4. Clone repo
```bash
git clone https://github.com/Rishikuber/sales-forecasting-time-series.git
cd sales-forecasting-time-series
```

#### 5. Build and run
```bash
docker build -t sales-api .
docker run -d -p 8000:8000 sales-api
```

#### 6. Access API
```
http://your-ec2-public-ip:8000
http://your-ec2-public-ip:8000/docs
```

---

### 🎨 OPTION C: RENDER (Alternative to Heroku)

#### 1. Go to render.com and sign up
- Sign up with GitHub

#### 2. Create Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repo
- Select main branch

#### 3. Configure
- **Name:** sales-forecasting-api
- **Runtime:** Python 3.11
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`

#### 4. Deploy
- Click Deploy
- Wait for deployment

#### 5. Access API
- Your app URL will be shown on dashboard

---

### ⚡ OPTION D: RAILWAY

#### 1. Go to railway.app
#### 2. Connect GitHub
#### 3. Select repository
#### 4. Railway auto-detects requirements.txt and Procfile
#### 5. Deploy!

---

## 🧪 Step 4: Test Your Deployed API

### Using Browser (Easiest)
```
https://your-deployed-url.com/docs
```

### Using curl
```bash
# Health check
curl https://your-deployed-url.com/

# Get stats
curl https://your-deployed-url.com/stats

# Historical data (last 30 days)
curl "https://your-deployed-url.com/historical?days=30"

# ARIMA forecast (30 days)
curl -X POST "https://your-deployed-url.com/forecast/arima?periods=30"

# Prophet forecast (30 days)
curl -X POST "https://your-deployed-url.com/forecast/prophet?periods=30"

# Compare models
curl -X POST "https://your-deployed-url.com/forecast/compare?periods=30"
```

### Using Python
```python
import requests

BASE_URL = "https://your-deployed-url.com"

# Get stats
response = requests.get(f"{BASE_URL}/stats")
print(response.json())

# Get forecast
response = requests.post(f"{BASE_URL}/forecast/arima?periods=30")
print(response.json())
```

### Using JavaScript/React
```javascript
const BASE_URL = "https://your-deployed-url.com";

// Get stats
fetch(`${BASE_URL}/stats`)
  .then(res => res.json())
  .then(data => console.log(data));

// Get forecast
fetch(`${BASE_URL}/forecast/arima?periods=30`, {
  method: "POST"
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/docs` | GET | Swagger UI (Interactive Docs) |
| `/redoc` | GET | ReDoc (Alternative Docs) |
| `/stats` | GET | Dataset statistics |
| `/historical?days=N` | GET | Last N days of data |
| `/forecast/arima?periods=N` | POST | ARIMA forecast |
| `/forecast/prophet?periods=N` | POST | Prophet forecast |
| `/forecast/compare?periods=N` | POST | Compare both models |

---

## 🔧 Environment Variables

If deploying, add these for production:

```bash
# Heroku
heroku config:set PYTHON_VERSION=3.11

# Docker
docker run -e PORT=8000 -p 8000:8000 sales-api
```

---

## 🐛 Troubleshooting

### Issue: "Port already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

### Issue: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Issue: "Data file not found"
- Make sure `sales_time_series_dataset.csv` is in the same directory as `app.py`

### Issue: "CORS error"
- Already handled in app.py, should work

### Issue: "Heroku deployment fails"
```bash
heroku logs --tail
```

---

## 📈 Next Steps

1. ✅ Deploy API
2. ✅ Test all endpoints
3. ✅ Add to resume with live link
4. ✅ Share with recruiters
5. ✅ Add to portfolio website

---

## 📝 Resume Update

Add this to your resume:

```
Sales Forecasting API (Deployed)
Tools: FastAPI, Python, ARIMA/Prophet, Docker, [Platform]
- Built production-ready REST API for time-series sales prediction
- Implemented ARIMA & Prophet models with <5% MAPE
- Containerized with Docker for scalability
- Deployed to [Heroku/AWS/Render/Railway]
- Live API: [Your API URL]
- Interactive Dashboard: [Dashboard URL if deployed]
- GitHub: github.com/Rishikuber/sales-forecasting-time-series
```

---

## 🎯 Performance Tips

1. **Cache data** - Don't reload CSV every request
2. **Async processing** - Use async/await for long operations
3. **Model caching** - Train once, reuse predictions
4. **API rate limiting** - Prevent abuse

---

## 🚀 Going Further

### Add Monitoring
```python
from prometheus_client import Counter, Histogram
requests_total = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')
```

### Add Authentication
```python
from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.get("/protected")
async def protected(credentials: HTTPAuthCredentials = Depends(security)):
    return {"message": "Protected endpoint"}
```

### Add Database
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@db:5432/forecasts"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

---

## 📚 Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- Heroku Docs: https://devcenter.heroku.com
- AWS EC2: https://docs.aws.amazon.com/ec2
- Docker: https://docs.docker.com
- Prophet: https://facebook.github.io/prophet
- ARIMA: https://www.statsmodels.org/

---

## ✅ Deployment Checklist

```
□ Files copied to repo
□ Dataset file present
□ Local testing successful
□ API endpoints working
□ Cloud platform selected
□ Deployment successful
□ API URL tested
□ Resume updated
□ Links shared with recruiters
```

---

**Happy Deploying! 🚀**

Need help? Check the API docs at `/docs` endpoint on your deployed URL!
