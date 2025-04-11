import streamlit as st
import numpy as np
import joblib
import os

# Page config
st.set_page_config(page_title="Concrete Strength Predictor", layout="centered")

# Title
st.markdown("""
    <h2 style='text-align: center; color: #003366;'>Concrete Compressive Strength Predictor</h2>
    <p style='text-align: center; font-size:16px; color: #555;'>
    <strong>Developed by:</strong> Mohamed K. Elshaarawy, Abdelrahman K. Hamed & Mostafa M. Alsaadawi
    </p>
""", unsafe_allow_html=True)

# Load model
model_path = os.path.join(os.path.dirname(__file__), "CGB.joblib")
try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# Input panel
st.markdown("---")
st.markdown("### 🧪 Input Parameters")

col1, col2 = st.columns(2)
with col1:
    x1 = st.number_input("X1: Cement (kg/m³)", min_value=0.0, format="%.2f")
    x2 = st.number_input("X2: Blast Furnace Slag (kg/m³)", min_value=0.0, format="%.2f")
    x3 = st.number_input("X3: Fly Ash (kg/m³)", min_value=0.0, format="%.2f")
    x4 = st.number_input("X4: Water (kg/m³)", min_value=0.0, format="%.2f")

with col2:
    x5 = st.number_input("X5: Superplasticizer (kg/m³)", min_value=0.0, format="%.2f")
    x6 = st.number_input("X6: Coarse Aggregate (kg/m³)", min_value=0.0, format="%.2f")
    x7 = st.number_input("X7: Fine Aggregate (kg/m³)", min_value=0.0, format="%.2f")
    x8 = st.number_input("X8: Age (days)", min_value=0.0, format="%.2f")

# Predict button
st.markdown("---")
if st.button("🔍 Predict Strength"):
    input_data = [x1, x2, x3, x4, x5, x6, x7, x8]

    if all(val == 0.0 for val in input_data):
        st.warning("⚠️ Please enter non-zero values for prediction.")
    else:
        try:
            prediction = model.predict([input_data])[0]
            st.markdown(f"""
                <div style='text-align:center; padding:20px; background-color:#f0f8ff; border-radius:10px;'>
                    <h3 style='color:#004d00;'>✅ Predicted Concrete Strength:</h3>
                    <h1 style='color:#0073e6;'>{prediction:.2f} MPa</h1>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
