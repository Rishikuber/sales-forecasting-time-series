import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.markdown("# 📈 Sales Forecasting Dashboard")
st.markdown("**Time-Series Analysis & Prediction**")

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('sales_time_series_dataset.csv')
    data['date'] = pd.to_datetime(data['date'])
    return data.sort_values('date')

# Train models
@st.cache_resource
def train_models(data):
    try:
        # ARIMA
        arima_model = ARIMA(data['sales'], order=(5, 1, 0)).fit()
        
        # Prophet
        prophet_data = data[['date', 'sales']].copy()
        prophet_data.columns = ['ds', 'y']
        prophet_model = Prophet(yearly_seasonality=True, interval_width=0.95)
        with st.spinner("Training Prophet..."):
            prophet_model.fit(prophet_data)
        
        return arima_model, prophet_model
    except Exception as e:
        st.error(f"Error training models: {str(e)}")
        return None, None

def calculate_mape(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100

# Load data
data = load_data()
st.success(f"✅ Loaded {len(data)} records from {data['date'].min().date()} to {data['date'].max().date()}")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    model_choice = st.radio(
        "Select Model:",
        ["ARIMA", "Prophet", "Compare Both"]
    )
    
    forecast_days = st.slider(
        "Forecast Days:",
        min_value=1,
        max_value=365,
        value=30,
        step=1
    )
    
    st.markdown("---")
    
    st.markdown("## 📊 Dataset Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Records", f"{len(data):,}")
        st.metric("Avg Daily Sales", f"₹{data['sales'].mean():,.0f}")
    with col2:
        st.metric("Max Sales", f"₹{data['sales'].max():,.0f}")
        st.metric("Min Sales", f"₹{data['sales'].min():,.0f}")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔮 Forecast", "📉 Analysis"])

# TAB 1: Overview
with tab1:
    st.markdown("### Historical Sales Trend")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['sales'],
        mode='lines',
        name='Actual Sales',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # 7-day rolling average
    data['rolling_7'] = data['sales'].rolling(7).mean()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['rolling_7'],
        mode='lines',
        name='7-Day Average',
        line=dict(color='#ff7f0e', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Sales Over Time",
        xaxis_title="Date",
        yaxis_title="Sales (₹)",
        hovermode='x unified',
        height=500,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

# TAB 2: Forecast
with tab2:
    if st.button("🚀 Generate Forecast", type="primary", use_container_width=True):
        with st.spinner("Training models and generating forecast..."):
            arima_model, prophet_model = train_models(data)
            
            if arima_model is None:
                st.stop()
            
            last_date = data['date'].max()
            future_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]
            
            # ARIMA
            if model_choice in ["ARIMA", "Compare Both"]:
                arima_forecast = arima_model.get_forecast(steps=forecast_days)
                arima_pred = arima_forecast.summary_frame()
                arima_values = arima_pred['mean'].values
                arima_lower = arima_pred['mean_ci_lower'].values
                arima_upper = arima_pred['mean_ci_upper'].values
            
            # Prophet
            if model_choice in ["Prophet", "Compare Both"]:
                future_df = prophet_model.make_future_dataframe(periods=forecast_days)
                prophet_pred = prophet_model.predict(future_df)
                prophet_pred = prophet_pred[prophet_pred['ds'] > last_date]
                prophet_values = prophet_pred['yhat'].values
                prophet_lower = prophet_pred['yhat_lower'].values
                prophet_upper = prophet_pred['yhat_upper'].values
            
            # Plot
            fig = go.Figure()
            
            # Historical
            fig.add_trace(go.Scatter(
                x=data['date'],
                y=data['sales'],
                mode='lines',
                name='Historical',
                line=dict(color='#1f77b4', width=2)
            ))
            
            # ARIMA
            if model_choice in ["ARIMA", "Compare Both"]:
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=arima_values,
                    mode='lines',
                    name='ARIMA Forecast',
                    line=dict(color='#ff7f0e', width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=future_dates + future_dates[::-1],
                    y=list(arima_upper) + list(arima_lower[::-1]),
                    fill='toself',
                    name='ARIMA CI',
                    fillcolor='rgba(255, 127, 14, 0.2)',
                    line=dict(color='rgba(255,255,255,0)')
                ))
            
            # Prophet
            if model_choice in ["Prophet", "Compare Both"]:
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=prophet_values,
                    mode='lines',
                    name='Prophet Forecast',
                    line=dict(color='#2ca02c', width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=future_dates + future_dates[::-1],
                    y=list(prophet_upper) + list(prophet_lower[::-1]),
                    fill='toself',
                    name='Prophet CI',
                    fillcolor='rgba(44, 160, 44, 0.2)',
                    line=dict(color='rgba(255,255,255,0)')
                ))
            
            fig.update_layout(
                title=f"Sales Forecast - Next {forecast_days} Days",
                xaxis_title="Date",
                yaxis_title="Sales (₹)",
                hovermode='x unified',
                height=600,
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display forecast table
            if model_choice == "ARIMA":
                st.markdown("### ARIMA Forecast Values")
                forecast_df = pd.DataFrame({
                    'Date': [d.strftime("%Y-%m-%d") for d in future_dates],
                    'Forecast': arima_values,
                    'Lower': arima_lower,
                    'Upper': arima_upper
                })
                st.dataframe(forecast_df, use_container_width=True)
            
            elif model_choice == "Prophet":
                st.markdown("### Prophet Forecast Values")
                forecast_df = pd.DataFrame({
                    'Date': [d.strftime("%Y-%m-%d") for d in future_dates],
                    'Forecast': prophet_values,
                    'Lower': prophet_lower,
                    'Upper': prophet_upper
                })
                st.dataframe(forecast_df, use_container_width=True)
            
            else:  # Compare
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### ARIMA Forecast")
                    forecast_df = pd.DataFrame({
                        'Date': [d.strftime("%Y-%m-%d") for d in future_dates],
                        'Forecast': arima_values
                    })
                    st.dataframe(forecast_df.head(15), use_container_width=True)
                
                with col2:
                    st.markdown("### Prophet Forecast")
                    forecast_df = pd.DataFrame({
                        'Date': [d.strftime("%Y-%m-%d") for d in future_dates],
                        'Forecast': prophet_values
                    })
                    st.dataframe(forecast_df.head(15), use_container_width=True)

# TAB 3: Analysis
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sales Distribution")
        fig = px.histogram(
            x=data['sales'],
            nbins=30,
            title="Distribution of Daily Sales"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Sales by Day of Week")
        data['dow'] = data['date'].dt.day_name()
        dow_avg = data.groupby('dow')['sales'].mean()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_avg = dow_avg.reindex([d for d in day_order if d in dow_avg.index])
        
        fig = px.bar(
            x=dow_avg.index,
            y=dow_avg.values,
            title="Avg Sales by Day of Week"
        )
        st.plotly_chart(fig, use_container_width=True)
