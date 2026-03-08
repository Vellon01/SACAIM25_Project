from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

app = FastAPI(
    title="Gold Price Prediction API",
    description="API for predicting gold prices using SARIMA and SVM models.",
    version="1.0.0"
)

# Load Models
try:
    sarima_model = joblib.load('sarima_model.pkl')
    svm_model = joblib.load('svm_linear_model.pkl')
except Exception as e:
    print(f"Error loading models: {e}")
    # We don't raise here so the app can still start and return 500s on prediction endpoints
    sarima_model = None
    svm_model = None

class SARIMARequest(BaseModel):
    n_periods: int = 1

class SVMRequest(BaseModel):
    features: list[float]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "features": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                }
            ]
        }
    }


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "models_loaded": {
            "sarima": sarima_model is not None,
            "svm": svm_model is not None
        }
    }

@app.post("/predict/sarima")
def predict_sarima(request: SARIMARequest):
    if sarima_model is None:
        raise HTTPException(status_code=500, detail="SARIMA model not loaded.")
    
    if request.n_periods <= 0:
        raise HTTPException(status_code=400, detail="n_periods must be greater than 0.")

    try:
        # Forecast n_periods into the future
        forecast = sarima_model.predict(n_periods=request.n_periods)
        
        # Depending on pmdarima version, predict might return a pandas Series or a numpy array
        if isinstance(forecast, pd.Series):
            forecast_list = forecast.tolist()
        else:
            forecast_list = forecast.tolist()

        return {
            "n_periods": request.n_periods,
            "forecast": forecast_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/svm")
def predict_svm(request: SVMRequest):
    if svm_model is None:
        raise HTTPException(status_code=500, detail="SVM model not loaded.")
    
    if len(request.features) != 6:
        raise HTTPException(status_code=400, detail=f"Expected exactly 6 features, got {len(request.features)}.")

    try:
        # SVR expects a 2D array
        features_array = np.array([request.features])
        prediction = svm_model.predict(features_array)
        
        return {
            "prediction": float(prediction[0]),
            "features_used": request.features
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
