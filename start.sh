#!/bin/bash
# Run the forecasting script
python /app/forecasting_wastewater.py
# Start MLflow UI
mlflow ui --host 0.0.0.0