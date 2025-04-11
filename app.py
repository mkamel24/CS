import streamlit as st
import numpy as np
import joblib
import os

# Set page config
st.set_page_config(page_title="Concrete Strength Predictor", layout="centered")

# App title and info
st.title("🧱 Concrete Compressive Strength Predictor")
st.markdown("**Developed by:** Mohamed K. Elshaarawy, Abdelrahman K. Hamed & Mostafa M. Alsaadawi")

# Load model
model_path = "C:/Users/asus1/Desktop/CGB.joblib"

if not os.path.exists(model_path):
    st.error("❌ Model file not found at the specified path.")
    st.stop()

try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# Input panel
st.subheader("🔢 Enter Mix Parameters")

col1, col2 = st.columns(2)

with col1:
    x1 = st.number_input("Cement (kg/m³)", min_value=0.0, format="%.2f")
    x2 = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, format="%.2f")
    x3 = st.number_input("Fly Ash (kg/m³)", min_value=0.0, format="%.2f")
    x4 = st.number_input("Water (kg/m³)", min_value=0.0, format="%.2f")

with col2:
    x5 = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, format="%.2f")
    x6 = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, format="%.2f")
    x7 = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, format="%.2f")
    x8 = st.number_input("Age (days)", min_value=0.0, format="%.2f")

# Predict button
if st.button("🔍 Predict Strength"):
    inputs = [x1, x2, x3, x4, x5, x6, x7, x8]
    if all(v == 0.0 for v in inputs):
        st.warning("⚠️ Please provide non-zero values for prediction.")
    else:
        try:
            prediction = model.predict([inputs])[0]
            st.success(f"🎯 **Predicted Concrete Strength:** {prediction:.2f} MPa")
        except Exception as e:
            st.error(f"❌ Prediction error: {e}")
