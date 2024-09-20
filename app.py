import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import time

# Load pickled objects
with open(r'label_encoders.pkl', 'rb') as file:
    encoder = pickle.load(file)

with open(r'scaler1.pkl', 'rb') as file:
    scaler = pickle.load(file)

with open(r'carprice.pkl', 'rb') as file:
    model = pickle.load(file)

# Apply CSS styling
st.markdown("""
<style>
h1 {
    color: red; /* Change to your desired color */
}
</style>
""", unsafe_allow_html=True)

def image_carousel(img_list, interval=2):
    """Displays a slideshow of images."""
    img_slot = st.empty()  # Create a placeholder for the images
    img_idx = 0  # Start index

    # Loop through images indefinitely
    while True:
        img_slot.image(img_list[img_idx], use_column_width=True)
        img_idx = (img_idx + 1) % len(img_list)  # Cycle through images
        time.sleep(interval)

def main():
    option = st.sidebar.radio("Options", ["Home", "App Page"])
    if option == "Home":
        st.title("About Car Dekho")
        st.write("""
        CarDekho.com is India's leading car search venture that helps users buy cars that are right for them. 
        Its website and app carry rich automotive content such as expert reviews, detailed specs and prices, 
        comparisons as well as videos and pictures of all car brands and models available in India. 
        The company has tie-ups with many auto manufacturers, more than 4000 car dealers, and numerous financial institutions to 
        facilitate the purchase of vehicles.
        """)
        # Layout for dashboard-like view
        col1, col2 = st.columns([2, 1])  # Create columns for a dashboard layout
        with col1:
            img_dir = "img"  # Replace with your image directory
            img_list = [os.path.join(img_dir, img) for img in os.listdir(img_dir) if img.endswith(('.jpg', '.png'))]
            image_carousel(img_list)  # Start the slideshow

    else:
        st.title("Car Dekho Price Prediction")

        bt = st.selectbox("Body Type", ["Select bodytype"] + ['Hatchback', 'SUV', 'Sedan', 'MUV', 'Minivans', 'Wagon'])
        km = st.slider("Kilo Meter", min_value=700, max_value=150000)
        trans = st.selectbox("Transmission", ["Select Transmission"] + ['Manual', 'Automatic'])
        owners = st.selectbox("No of Owners", ["Select no.of.owner"] + [0, 1, 2, 3, 4, 5])
        brand = st.selectbox("Brand", ["Select Brand"] + ['Maruti', 'Ford', 'Tata', 'Hyundai', 'Datsun', 'Honda', 'Renault', 
                                                          'Volkswagen', 'Mahindra', 'Skoda', 'MG', 'Kia', 'Toyota', 'Nissan', 
                                                          'Fiat', 'Chevrolet', 'Citroen', 'Mini', 'Hindustan Motors'])

        model_year = st.slider("Model Year", min_value=1985, max_value=2023)
        insurance = st.selectbox("Insurance Validity", ["Select Insurance Validity"] + ['Third Party insurance', 
                                                                                          'Comprehensive', 'Zero Dep', 'Not Available'])
        fueltype = st.selectbox("Fuel Type", ["Select Fuel Type"] + ['Petrol', 'Diesel', 'LPG', 'CNG'])
        mileage = st.slider("Mileage", min_value=10.0, max_value=28.0)
        color = st.selectbox("Color", ["Select Color"] + ['white', 'red', 'others', 'gray', 'maroon', 'orange', 'silver', 
                                                           'blue', 'brown', 'yellow', 'black', 'gold', 'green', 'purple'])
        gears = st.selectbox("Gear Box", ["Select Gears"] + [5, 7, 4, 6, 0, 8])
        no_door_numbers = st.number_input("Number of Doors", min_value=1, value=4)
        city = st.selectbox("City", ["Select City"] + ['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Jaipur', 'Kolkata'])

        details1 = []

        # Assuming the first few inputs are dynamic and the rest are constants
        if bt != "Select bodytype":
            encoded_value = encoder["bt"].transform([bt])[0]
            details1.append(int(encoded_value))
        else:
            st.warning("Please choose a valid option in the body type box")

        # Dynamic input for kilometer
        details1.append(km)

        # Dynamic input for transmission
        if trans != "Select Transmission":
            encoded_value = encoder["transmission"].transform([trans])[0]
            details1.append(int(encoded_value))
        else:
            st.warning("Please choose a valid option in the transmission box")

        # Dynamic input for number of owners
        details1.append(owners)

        # Dynamic input for brand
        if brand != "Select Brand":
            encoded_value = encoder["oem"].transform([brand])[0]
            details1.append(int(encoded_value))
        else:
            st.warning("Please choose a valid option in the brand box")

        # Dynamic input for model year
        details1.append(float(model_year))

        # Dynamic input for insurance
        if insurance != "Select Insurance Validity":
            encoded_value = encoder["Insurance Validity"].transform([insurance])[0]
            details1.append(int(encoded_value))
        else:
            st.warning("Please choose a valid option in the insurance box")

        # Dynamic input for fuel type
        if fueltype != "Select Fuel Type":
            encoded_value = encoder["Fuel Type"].transform([fueltype])[0]
            details1.append(int(encoded_value))
        else:
            st.warning("Please choose a valid option in the fuel type box")

        # Dynamic input for mileage
        details1.append(mileage)

        # Constant values
        max_power_mean = 83.284
        torque_mean = 127.384
        Length_mean = 3880.395
        Width_mean = 1690.101
        Height_mean = 1542.333
        wheelbase_mean = 2465.064

        # Append constant values
        details1.extend([
            max_power_mean,  # 9
            torque_mean,     # 10
            4,               # No of Cylinder (constant)
            1,               # Values per Cylinder (constant)
            Length_mean,     # Length
            Width_mean,      # Width
            Height_mean,     # Height
            wheelbase_mean,  # Wheel Base
            3,               # Steering Type (constant)
            0,               # Front Brake Type (constant)
            0,               # Rear Brake Type (constant)
            4,               # Tyre Type (constant)
            1                # No Door Numbers (constant)
        ])

        # Dynamic input for gears
        if gears != "Select Gears":
            details1.append(gears)
        else:
            st.warning("Please choose a valid option in the gears box")

        # City encoding
        if city != "Select City":
            if "City" in encoder:  # Check for the key in encoder
                encoded_value = encoder["City"].transform([city])[0]
                details1.append(int(encoded_value))
            else:
                st.warning("City encoder not found.")
        else:
            st.warning("Please choose a valid option for city.")

        # Log the final length of details1
        st.write(f"Length of details1: {len(details1)}")

        # Convert to DataFrame and scale
        details = [details1]
        values_scaled = None

    if st.button("Predict Price"):
    # Check if the length of details1 is 24 (i.e., all inputs are gathered)
        if len(details1) == 24:
        # Scale the data
          values_scaled = scaler.transform(details)
        
           # Make prediction
          prediction = model.predict(values_scaled)
          predicted_price = prediction[0].item() if len(prediction) > 0 else 0
          st.success(f"The predicted price is: {predicted_price:.2f}")
        else:
          st.warning("Please provide all inputs to get a valid prediction.")

    else:
          st.warning("Please provide all inputs to get a valid prediction.")

if __name__ == "__main__":
    main()
