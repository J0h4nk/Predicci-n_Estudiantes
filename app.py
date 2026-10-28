from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Cargar archivos del modelo generados en Colab
scaler = joblib.load('scaler.pkl')
model = joblib.load('mlp_model.pkl')

class StudentFeatures(BaseModel):
    Tareas: float
    Examenes: float
    Asistencia: float
    Estudio_Horas: float
    Sueno_Horas: float
    Extracurriculares: int

@app.post("/predict")
def predict_approval(data: StudentFeatures):
    input_data = np.array([[
        data.Tareas, data.Examenes, data.Asistencia,
        data.Estudio_Horas, data.Sueno_Horas, data.Extracurriculares
    ]])
    scaled_data = scaler.transform(input_data)
    prediction = model.predict(scaled_data)[0]
    probability = model.predict_proba(scaled_data)[0][1]
    
    return {
        "aprobado": int(prediction),
        "estado": "Aprobado" if prediction == 1 else "Reprobado",
        "probabilidad_aprobacion": round(float(probability), 4)
    }
