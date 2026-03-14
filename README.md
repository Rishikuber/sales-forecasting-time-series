# sales-forecasting-time-series
Time-series sales forecasting project using ARIMA and Prophet models
# Sales Forecasting using Time-Series Analysis

## Project Overview

This project develops a time-series forecasting model to predict future sales trends using more than two years of historical sales data. The objective is to analyze demand patterns, detect seasonality, and generate accurate forecasts that can support business planning and decision-making.

## Objectives

* Analyze historical sales data to identify trends and seasonal patterns
* Build forecasting models to predict future sales
* Evaluate model performance using statistical metrics
* Generate visual insights to support business strategy

## Tools and Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Statsmodels
* Prophet
* Scikit-learn

## Dataset

The dataset contains over **2 years of daily sales data** with the following fields:

| Column | Description          |
| ------ | -------------------- |
| date   | Date of sales record |
| sales  | Daily sales value    |

## Methodology

### 1. Data Preprocessing

* Converted date column to datetime format
* Set date as time-series index
* Checked and handled missing values

### 2. Exploratory Data Analysis (EDA)

* Visualized sales trends over time
* Identified seasonal patterns
* Used rolling averages to analyze long-term trends

### 3. Seasonal Decomposition

Decomposed the time series into:

* Trend
* Seasonality
* Residual components

### 4. Forecasting Models

Two forecasting models were implemented:

**ARIMA Model**

* Captures autoregressive and moving average patterns
* Used ARIMA(5,1,0) configuration

**Prophet Model**

* Handles trend and seasonality automatically
* Suitable for business time-series forecasting

### 5. Model Evaluation

Model performance was evaluated using **Mean Absolute Percentage Error (MAPE)**.

| Model                     | MAPE  |
| ------------------------- | ----- |
| ARIMA                     | 4.23% |
| Moving Average (Baseline) | ~7–9% |

Lower MAPE indicates higher forecasting accuracy.

## Results

* The ARIMA model achieved **MAPE = 4.23%**, indicating strong predictive performance.
* Clear weekly seasonality patterns were observed.
* Sales show a gradual increasing trend over time.

## Business Insights

* Demand fluctuates across different days of the week.
* Sales exhibit a consistent upward growth trend.
* Forecasting models can help businesses plan inventory and optimize supply chain decisions.

## Project Structure

sales-forecasting-time-series
│
├── sales_forecasting.ipynb
├── sales_time_series_dataset.csv
├── requirements.txt
└── README.md

## Future Improvements

* Implement LSTM deep learning forecasting models
* Integrate interactive dashboards using Tableau or Power BI
* Add external factors such as promotions and holidays to improve forecasting accuracy

## Author

Data Science Portfolio Project
