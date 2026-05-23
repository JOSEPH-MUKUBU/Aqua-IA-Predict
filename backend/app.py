from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import random

app = FastAPI(title="Water Quality API - Defi 2")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
base_dir = os.path.dirname(__file__)
cause_model_path = os.path.join(base_dir, 'models', 'cause_classifier.joblib')
risk_model_path = os.path.join(base_dir, 'models', 'risk_regressor.joblib')

try:
    cause_classifier = joblib.load(cause_model_path)
    risk_regressor = joblib.load(risk_model_path)
except Exception as e:
    print(f"Erreur de chargement des modeles: {e}")
    cause_classifier = None
    risk_regressor = None

class SensorData(BaseModel):
    ph: float
    turbidity: float
    conductivity: float
    chlorine: float
    temperature: float
    pressure: float
    flow: float

@app.post("/predict")
def predict_water_quality(data: SensorData):
    if not cause_classifier or not risk_regressor:
        raise HTTPException(status_code=500, detail="Modeles non charges")
        
    df = pd.DataFrame([data.dict()])
    
    # Predictions
    # Cause classifier
    cause_pred = cause_classifier.predict(df)[0]
    
    # Risk regressor
    risk_pred = risk_regressor.predict(df)[0]
    
    # Determination de l'alerte
    alert_level = "Vert"
    if risk_pred > 75 or cause_pred == 'Contamination':
        alert_level = "Rouge"
    elif risk_pred > 40 or cause_pred != 'Normal':
        alert_level = "Jaune"
        
    return {
        "Risk_Index": round(risk_pred, 2),
        "Probable_Cause": cause_pred,
        "Alert_Level": alert_level
    }

@app.get("/simulate")
def get_simulated_data():
    # Helper to feed frontend with random simualted data based on random conditions
    # Base probabilities for conditions
    condition = random.choices(
        ['Normal', 'Stagnation', 'Corrosion', 'Contamination', 'Pression Faible'],
        weights=[0.7, 0.05, 0.1, 0.05, 0.1]
    )[0]
    
    if condition == 'Normal':
        ph = np.random.normal(7.2, 0.3)
        turbidity = max(0.1, np.random.normal(0.5, 0.2))
        conductivity = np.random.normal(400, 100)
        chlorine = np.random.normal(1.0, 0.3)
        temperature = np.random.normal(15, 3)
        pressure = np.random.normal(3.0, 0.3)
        flow = np.random.normal(300, 50)
    elif condition == 'Stagnation':
        ph = np.random.normal(7.5, 0.4)
        turbidity = np.random.normal(1.2, 0.5)
        conductivity = np.random.normal(450, 100)
        chlorine = max(0.0, np.random.normal(0.1, 0.1))
        temperature = np.random.normal(22, 2)
        pressure = np.random.normal(2.5, 0.3)
        flow = max(10, np.random.normal(30, 10))
    elif condition == 'Corrosion':
        ph = min(6.4, np.random.normal(6.0, 0.4))
        turbidity = np.random.normal(2.5, 0.8)
        conductivity = np.random.normal(900, 200)
        chlorine = np.random.normal(0.8, 0.3)
        temperature = np.random.normal(16, 3)
        pressure = np.random.normal(2.8, 0.4)
        flow = np.random.normal(250, 60)
    elif condition == 'Contamination':
        ph = np.random.normal(7.0, 0.8)
        turbidity = np.random.normal(6.0, 2.0)
        conductivity = np.random.normal(1200, 300)
        chlorine = max(0.0, np.random.normal(0.05, 0.05))
        temperature = np.random.normal(18, 4)
        pressure = np.random.normal(2.9, 0.3)
        flow = np.random.normal(300, 50)
    elif condition == 'Pression Faible':
        ph = np.random.normal(7.2, 0.3)
        turbidity = np.random.normal(0.8, 0.3)
        conductivity = np.random.normal(400, 100)
        chlorine = np.random.normal(0.9, 0.3)
        temperature = np.random.normal(15, 3)
        pressure = max(0.5, np.random.normal(1.2, 0.3))
        flow = max(20, np.random.normal(80, 20))

    return {
        "ph": round(max(0, min(14, ph)), 2),
        "turbidity": round(max(0, turbidity), 2),
        "conductivity": round(max(0, conductivity), 2),
        "chlorine": round(max(0, chlorine), 2),
        "temperature": round(max(-10, min(50, temperature)), 2),
        "pressure": round(max(0, pressure), 2),
        "flow": round(max(0, flow), 2),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
