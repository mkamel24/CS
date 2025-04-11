import streamlit as st
import numpy as np
import joblib
from PIL import Image
import requests
import os

# URLs for GitHub-hosted files
image_url = "https://raw.githubusercontent.com/mkamel24/CS/main/image.jpg"
model_url = "https://github.com/mkamel24/CS/raw/main/catboost.joblib"

# Local file paths
image_path = "image.jpg"
model_path = "catboost.joblib"

# Function to download files if they don't exist
def download_file(url, local_path):
    if not os.path.exists(local_path):
        r = requests.get(url)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(r.content)
        else:
            st.error(f"Failed to download file from {url} (HTTP {r.status_code})")
            st.stop()

# Download image and model
download_file(image_url, image_path)
download_file(model_url, model_path)

# Load and show the image
try:
    image = Image.open(image_path)
    st.image(image, use_container_width=True)
except Exception as e:
    st.error(f"Image could not be loaded: {e}")

# Titles
st.markdown("<h2 style='color:#0000FF;'>GUI model for Predicting Concrete CS Based on 7 Ingredients & Curing Age</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#C00000;'>Developed by: Mohamed K. Elshaarawy, Abdelrahman K. Hamed & Mostafa M. Alsaadawi</h4>", unsafe_allow_html=True)

# Load model with error handling
try:
    model_catb = joblib.load(model_path)
    if not hasattr(model_catb, "predict"):
        raise ValueError("Loaded object is not a valid model.")
except Exception as e:
    st.error(f"Model could not be loaded: {e}")
    st.info("Try running this app in an environment with compatible numpy, joblib, and catboost versions.")
    st.stop()

# Parameter input section
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

# Prediction
if st.button("Calculate"):
    input_values = [entries[key] for key in params.values()]
    if all(v == 0 for v in input_values):
        st.warning("Please enter at least one value greater than zero.")
    else:
        try:
            input_data = np.array([input_values])
            prediction = model_catb.predict(input_data)
            st.success(f"Concrete Compressive Strength (CS) = {prediction[0]:.4f} MPa")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
