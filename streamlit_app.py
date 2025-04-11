import streamlit as st
import numpy as np
import joblib
import os

# Set page config
st.set_page_config(page_title="Concrete Strength Predictor", layout="centered")

# Load CatBoost model
model_path = os.path.join(os.path.dirname(__file__), "CGB.joblib")
try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# App title
st.title("🧱 Concrete Compressive Strength Predictor")
st.markdown("""
Developed by: **Mohamed K. Elshaarawy**, **Abdelrahman K. Hamed**, and **Mostafa M. Alsaadawi**  
Enter mix ingredients below to predict the compressive strength of concrete.
""")

# Input fields
st.header("🔢 Input Parameters")

cols = st.columns(2)
X1 = cols[0].number_input("X1: Cement (kg/m³)", min_value=0.0, format="%.2f")
X2 = cols[1].number_input("X2: Blast Furnace Slag (kg/m³)", min_value=0.0, format="%.2f")
X3 = cols[0].number_input("X3: Fly Ash (kg/m³)", min_value=0.0, format="%.2f")
X4 = cols[1].number_input("X4: Water (kg/m³)", min_value=0.0, format="%.2f")
X5 = cols[0].number_input("X5: Superplasticizer (kg/m³)", min_value=0.0, format="%.2f")
X6 = cols[1].number_input("X6: Coarse Aggregate (kg/m³)", min_value=0.0, format="%.2f")
X7 = cols[0].number_input("X7: Fine Aggregate (kg/m³)", min_value=0.0, format="%.2f")
X8 = cols[1].number_input("X8: Age (days)", min_value=0.0, format="%.2f")

inputs = [X1, X2, X3, X4, X5, X6, X7, X8]

# Predict button
if st.button("🚀 Predict Strength"):
    if all(val > 0 for val in inputs):
        try:
            prediction = model.predict([inputs])[0]
            st.success(f"✅ Predicted Concrete Strength: **{prediction:.2f} MPa**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
    else:
        st.warning("⚠️ Please enter all positive values to get a prediction.")
