import streamlit as st
import joblib
import os
import numpy as np
from PIL import Image

# Load CatBoost model
model_path = os.path.join(os.path.dirname(__file__), "catboost.joblib")
try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# Display image if available
image_path = os.path.join(os.path.dirname(__file__), "image.jpg")
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, caption="Concrete Mix", use_container_width=True)

# App Title
st.title("Concrete Compressive Strength Predictor")

# Input fields
st.subheader("Enter Mix Details:")
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

# Prediction
if st.button("Predict"):
    inputs = [x1, x2, x3, x4, x5, x6, x7, x8]
    if all(val == 0 for val in inputs):
        st.warning("Please enter at least one non-zero value.")
    else:
        try:
            prediction = model.predict([inputs])[0]
            st.success(f"Predicted Strength: {prediction:.4f} MPa")
        except Exception as e:
            st.error(f"Prediction error: {e}")
