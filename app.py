import streamlit as st
import numpy as np
import joblib
from PIL import Image
import os

# Set page title and layout
st.set_page_config(page_title="Concrete Strength Predictor", layout="centered")

# Load image
image_path = "C:/Users/asus1/Desktop/image.jpg"
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, use_column_width=True)
else:
    st.error(f"Image file not found at: {image_path}")

# Title and authors
st.markdown("<h2 style='color:#0000FF;'>GUI model for Predicting Concrete CS Based on 7 Ingredients & Curing Age</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#C00000;'>Developed by: Mohamed K. Elshaarawy, Abdelrahman K. Hamed & Mostafa M. Alsaadawi</h4>", unsafe_allow_html=True)

# Load model
model_path_catb = "C:/Users/asus1/Desktop/catboost.joblib"
if not os.path.exists(model_path_catb):
    st.error("CatBoost model file not found.")
    st.stop()

model_catb = joblib.load(model_path_catb)

# Parameters
st.subheader("Definition of Parameters")
params = {
    "X1: Cement (kg/m³)": "X1",
    "X2: Blast Furnace Slag (kg/m³)": "X2",
    "X3: Fly Ash (kg/m³)": "X3",
    "X4: Water (kg/m³)": "X4",
    "X5: Superplasticizer (kg/m³)": "X5",
    "X6: Coarse Aggregate (kg/m³)": "X6",
    "X7: Fine Aggregate (kg/m³)": "X7",
    "X8: Age (day)": "X8"
}

entries = {}
for label, key in params.items():
    entries[key] = st.number_input(label, min_value=0.0, format="%.2f")

# Predict button
if st.button("Calculate"):
    input_values = [entries[key] for key in params.values()]

    # Check if all values are zero
    if all(value == 0 for value in input_values):
        st.warning("Please enter at least one value greater than zero.")
    else:
        input_data = np.array([input_values])
        try:
            prediction = model_catb.predict(input_data)
            st.success(f"Concrete Compressive Strength (CS) = {prediction[0]:.4f} MPa")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
