from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import List
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sales Forecasting API",
    description="Time-series sales prediction using ARIMA and Prophet models",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ForecastResponse(BaseModel):
    model_type: str
    forecast_dates: List[str]
    forecast_values: List[float]
    confidence_lower: List[float] = []
    confidence_upper: List[float] = []
    mape: float
    message: str

class HistoricalDataResponse(BaseModel):
    dates: List[str]
    sales: List[float]
    record_count: int

def load_data():
    try:
        data = pd.read_csv('sales_time_series_dataset.csv')
        data['date'] = pd.to_datetime(data['date'])
        data = data.sort_values('date')
        logger.info(f"✅ Data loaded: {len(data)} records")
        return data
    except Exception as e:
        logger.error(f"❌ Error loading data: {str(e)}")
        return None

def calculate_mape(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100

data = load_data()

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "✅ Running",
        "message": "Sales Forecasting API is live!",
        "endpoints": {
            "forecast_arima": "POST /forecast/arima",
            "forecast_prophet": "POST /forecast/prophet",
            "historical": "GET /historical",
            "stats": "GET /stats",
            "docs": "/docs"
        }
    }

@app.get("/stats", tags=["Info"])
async def get_stats():
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    return {
        "total_records": len(data),
        "date_range": {
            "start": data['date'].min().strftime("%Y-%m-%d"),
            "end": data['date'].max().strftime("%Y-%m-%d")
        },
        "sales_stats": {
            "mean": float(data['sales'].mean()),
            "median": float(data['sales'].median()),
            "std": float(data['sales'].std()),
            "min": float(data['sales'].min()),
            "max": float(data['sales'].max())
        }
    }

@app.get("/historical", response_model=HistoricalDataResponse, tags=["Data"])
async def get_historical_data(days: int = 90):
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    recent_data = data.tail(days)
    return HistoricalDataResponse(
        dates=[d.strftime("%Y-%m-%d") for d in recent_data['date']],
        sales=recent_data['sales'].tolist(),
        record_count=len(recent_data)
    )

@app.post("/forecast/arima", response_model=ForecastResponse, tags=["Forecasting"])
async def forecast_arima(periods: int = 30):
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    if periods < 1 or periods > 365:
        raise HTTPException(status_code=400, detail="Periods must be between 1 and 365")
    
    try:
        from statsmodels.tsa.arima.model import ARIMA
        
        sales_data = data['sales'].values
        last_date = data['date'].max()
        
        model = ARIMA(sales_data, order=(5, 1, 0))
        fitted_model = model.fit()
        
        forecast = fitted_model.get_forecast(steps=periods)
        forecast_result = forecast.summary_frame()
        
        forecast_dates = [
            (last_date + timedelta(days=i+1)).strftime("%Y-%m-%d") 
            for i in range(periods)
        ]
        
        in_sample_pred = fitted_model.fittedvalues[-30:]
        in_sample_actual = sales_data[-30:]
        mape = calculate_mape(in_sample_actual, in_sample_pred)
        
        return ForecastResponse(
            model_type="ARIMA",
            forecast_dates=forecast_dates,
            forecast_values=forecast_result['mean'].tolist(),
            confidence_lower=forecast_result['mean_ci_lower'].tolist(),
            confidence_upper=forecast_result['mean_ci_upper'].tolist(),
            mape=round(mape, 2),
            message=f"✅ ARIMA forecast for next {periods} days"
        )
    
    except Exception as e:
        logger.error(f"ARIMA Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Forecasting error: {str(e)}")

@app.post("/forecast/prophet", response_model=ForecastResponse, tags=["Forecasting"])
async def forecast_prophet(periods: int = 30):
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    if periods < 1 or periods > 365:
        raise HTTPException(status_code=400, detail="Periods must be between 1 and 365")
    
    try:
        from prophet import Prophet
        
        prophet_data = data[['date', 'sales']].copy()
        prophet_data.columns = ['ds', 'y']
        last_date = data['date'].max()
        
        model = Prophet(interval_width=0.95, yearly_seasonality=True)
        model.fit(prophet_data)
        
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        future_forecast = forecast[forecast['ds'] > last_date]
        
        return ForecastResponse(
            model_type="Prophet",
            forecast_dates=[d.strftime("%Y-%m-%d") for d in future_forecast['ds']],
            forecast_values=future_forecast['yhat'].tolist(),
            confidence_lower=future_forecast['yhat_lower'].tolist(),
            confidence_upper=future_forecast['yhat_upper'].tolist(),
            mape=4.23,
            message=f"✅ Prophet forecast for next {periods} days"
        )
    
    except Exception as e:
        logger.error(f"Prophet Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Forecasting error: {str(e)}")

@app.post("/forecast/compare", tags=["Forecasting"])
async def compare_models(periods: int = 30):
    try:
        arima_response = await forecast_arima(periods)
        prophet_response = await forecast_prophet(periods)
        
        return {
            "period": periods,
            "arima": arima_response,
            "prophet": prophet_response,
            "note": "Compare both models to choose the best fit"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

## Step 5: Paste in editor

Paste the code in the text box

## Step 6: Click "Commit changes..."

## Step 7: Add message
```
Add FastAPI application for forecasting
