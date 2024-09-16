import joblib
import pandas as pd
import streamlit as st

# Load the pipeline (which includes preprocessing and the model)
pipeline = joblib.load('gradient_boost_pipeline.pkl')

st.title("Car Price Prediction App")

# Sidebar for user inputs
st.sidebar.header("Input Features")

# Input features
model_year = st.sidebar.slider('Model Year', 2000, 2023, 2015)
mileage = st.sidebar.number_input('Mileage (in km)', min_value=0, step=1000)
power_rto = st.sidebar.number_input('Power (in cc)', min_value=800, step=100)
fuel_type = st.sidebar.selectbox('Fuel Type', ['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric'])
transmission = st.sidebar.selectbox('Transmission', ['Manual', 'Automatic'])

# Create DataFrame for model input
input_data = pd.DataFrame({
    'modelYear': [model_year],
    'Mileage': [mileage],
    'Power_RTO': [power_rto],
    'Fuel Type': [fuel_type],
    'transmission': [transmission]
})

# Display the input data
st.write("Input Data:")
st.write(input_data)

# Predict price
if st.button('Predict Price'):
    try:
        # Predict using the pipeline
        prediction = pipeline.predict(input_data)
        rounded_price = round(prediction[0], 2)
        st.write(f"Predicted Price: ₹{rounded_price}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
