# app/api/kpi_forecasting_router.py

from fastapi import APIRouter, UploadFile, File
import pandas as pd
from io import StringIO
from sklearn.linear_model import LinearRegression
import numpy as np

router = APIRouter()

@router.post("/upload_csv_forecast")
async def upload_csv_forecast(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(StringIO(content.decode("utf-8")))

    if "Date" not in df.columns or "KPI_Value" not in df.columns:
        return {"error": "CSV must contain 'Date' and 'KPI_Value' columns"}

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df["DayIndex"] = (df["Date"] - df["Date"].min()).dt.days

    X = df[["DayIndex"]]
    y = df["KPI_Value"]

    model = LinearRegression()
    model.fit(X, y)

    # Forecast next 5 days
    future_days = np.array([[i] for i in range(df["DayIndex"].max() + 1, df["DayIndex"].max() + 6)])
    predictions = model.predict(future_days)

    future_dates = pd.date_range(df["Date"].max() + pd.Timedelta(days=1), periods=5)

    forecast_result = [
        {"date": str(date.date()), "predicted_kpi": float(pred)}
        for date, pred in zip(future_dates, predictions)
    ]

    return {"forecast": forecast_result}


@router.post("/upload_csv_anomaly")
async def upload_csv_anomaly(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(StringIO(content.decode("utf-8")))

    if "KPI_Value" not in df.columns:
        return {"error": "CSV must contain 'KPI_Value' column"}

    mean = df["KPI_Value"].mean()
    std = df["KPI_Value"].std()

    df["Anomaly"] = ((df["KPI_Value"] > mean + 2*std) | (df["KPI_Value"] < mean - 2*std))
    anomalies = df[df["Anomaly"]]

    return {
        "anomalies": anomalies.to_dict(orient="records"),
        "mean": mean,
        "std_dev": std
    }
