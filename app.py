import streamlit as st
import joblib
import os
from PIL import Image
import numpy as np

# Set page configuration
st.set_page_config(page_title="Concrete Strength Predictor", layout="centered")

# Load the CatBoost model
model_path = os.path.join(os.path.dirname(__file__), "catboost.joblib")
if not os.path.exists(model_path):
    st.error("Model file not found. Please ensure catboost.joblib is in the same directory as this app.")
    st.stop()

try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# Load and display image
image_path = os.path.join(os.path.dirname(__file__), "image.jpg")
if os.path.exists(image_path):
    image = Image.open(image_path)
    scale_ratio = 0.6
    new_size = (int(image.width * scale_ratio), int(image.height * scale_ratio))
    resized_image = image.resize(new_size)
    st.image(resized_image, caption="Concrete Mix Illustration", use_container_width=False)

# Title and developer info with styled HTML
st.markdown("""
    <h2 style='text-align: center; font-family: Georgia, serif; color: #2F4F4F;'>
        Predicting Concrete Compressive Strength (MPa)
    </h2>
    <p style='text-align: center; font-size:16px; font-family:Courier New; color: #555;'>
        <strong>Using Machine Learning (CatBoost Model)</strong><br>
        Developers: <em>Mohamed K. Elshaarawy, Abdelrahman K. Hamed & Mostafa M. Alsaadawi</em>
    </p>
""", unsafe_allow_html=True)

# Input section
st.markdown("<h4 style='font-family:Verdana; color:#003366;'>Input Parameters</h4>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    x1 = st.number_input("X1: Cement (kg/m³)", min_value=0.0, format="%.2f", key="x1")
    x2 = st.number_input("X2: Blast Furnace Slag (kg/m³)", min_value=0.0, format="%.2f", key="x2")
    x3 = st.number_input("X3: Fly Ash (kg/m³)", min_value=0.0, format="%.2f", key="x3")
    x4 = st.number_input("X4: Water (kg/m³)", min_value=0.0, format="%.2f", key="x4")

with col2:
    x5 = st.number_input("X5: Superplasticizer (kg/m³)", min_value=0.0, format="%.2f", key="x5")
    x6 = st.number_input("X6: Coarse Aggregate (kg/m³)", min_value=0.0, format="%.2f", key="x6")
    x7 = st.number_input("X7: Fine Aggregate (kg/m³)", min_value=0.0, format="%.2f", key="x7")
    x8 = st.number_input("X8: Age (days)", min_value=0.0, format="%.2f", key="x8")

# Prediction logic
if st.button("Predict"):
    input_values = [x1, x2, x3, x4, x5, x6, x7, x8]

    if all(v == 0 for v in input_values):
        st.warning("Please enter non-zero values for at least one input to make a prediction.")
    else:
        try:
            prediction = model.predict([input_values])[0]
            st.success(f"Predicted Concrete Compressive Strength: **{prediction:.4f} MPa**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
