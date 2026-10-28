import streamlit as st
import requests

st.title("🎓 Predicción de Aprobación de Estudiantes (MLP)")

st.write("Ingrese los datos del estudiante para consultar la predicción:")

tareas = st.slider("Calificación Tareas (0-100)", 0.0, 100.0, 75.0)
examenes = st.slider("Calificación Exámenes (0-100)", 0.0, 100.0, 70.0)
asistencia = st.slider("Asistencia (%)", 0.0, 100.0, 85.0)
estudio = st.number_input("Horas de Estudio Semanales", 0.0, 50.0, 10.0)
sueno = st.number_input("Horas de Sueño Diarias", 0.0, 12.0, 7.0)
extracurriculares = st.selectbox("¿Participa en actividades extracurriculares?", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")

# URL DE TU ENDPOINT EN RENDER
API_URL = "https://predicci-n-estudiantes.onrender.com/predict"

if st.button("Predecir Aprobación"):
    payload = {
        "Tareas": tareas,
        "Examenes": examenes,
        "Asistencia": asistencia,
        "Estudio_Horas": estudio,
        "Sueno_Horas": sueno,
        "Extracurriculares": extracurriculares
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        if response.status_code == 200:
            res_data = response.json()
            if res_data["aprobado"] == 1:
                st.success(f"Resultado: **{res_data['estado']}** (Probabilidad: {res_data['probabilidad_aprobacion']*100:.1f}%)")
            else:
                st.error(f"Resultado: **{res_data['estado']}** (Probabilidad: {res_data['probabilidad_aprobacion']*100:.1f}%)")
        else:
            st.error(f"Error HTTP {response.status_code}: {response.text}")
    except requests.exceptions.Timeout:
        st.warning("El servidor está activándose en Render. Espera unos segundos y vuelve a hacer clic.")
    except Exception as e:
        st.error(f"Error al conectar con el End-point: {e}")