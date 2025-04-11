import streamlit as st
import joblib
import os
import numpy as np
from PIL import Image

# Set page title and layout
st.set_page_config(page_title="Concrete Strength Predictor", layout="centered")

# Paths to local model and image
model_path = os.path.join(os.path.dirname(__file__), "catboost.joblib")
image_path = os.path.join(os.path.dirname(__file__), "image.jpg")

# Load model
try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# Load and display image
if os.path.exists(image_path):
    img = Image.open(image_path)
    st.image(img, caption="Concrete Mix Illustration", use_container_width=True)

# App title and credits
st.markdown("""
    <h2 style='text-align: center; color: #2F4F4F;'>Concrete Compressive Strength Predictor</h2>
    <p style='text-align: center; font-size:16px; color: #555;'>
        <strong>Using CatBoost Regression Model</strong><br>
        <em>Developed by Mohamed K. Elshaarawy, Abdelrahman K. Hamed & Mostafa M. Alsaadawi</em>
    </p>
""", unsafe_allow_html=True)

# Input section
st.header("Enter Concrete Mix Details")

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

# Prediction button
if st.button("Predict"):
    inputs = [x1, x2, x3, x4, x5, x6, x7, x8]

    if all(val == 0 for val in inputs):
        st.warning("Please enter values greater than zero.")
    else:
        try:
            prediction = model.predict([inputs])[0]
            st.success(f"Predicted Compressive Strength: **{prediction:.4f} MPa**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
