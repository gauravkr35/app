import streamlit as st
import pandas as pd
import joblib

# ✅ Must be first Streamlit command
st.set_page_config(page_title="Used Car Price Predictor", layout="centered")

# Dummy login credentials
USER_CREDENTIALS = {
    "admin": "demo",
    "gaurav": "1234",
}

# Session state to track login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🔐 Login Function
def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

# If not logged in, show login
if not st.session_state.logged_in:
    login()
    st.stop()

# ✅ Load trained model after login
model = joblib.load("car_price_model_compressed.pkl")

st.title("🚗 Used Car Price Predictor")
st.write("Enter your car's details below to estimate its selling price.")

# Car model list
model_list = ['Alto', 'Grand', 'i20', 'Ecosport', 'Wagon R', 'i10', 'Venue',
   'Swift', 'Verna', 'Duster', 'Cooper', 'Ciaz', 'C-Class', 'Innova',
   'Baleno', 'Swift Dzire', 'Vento', 'Creta', 'City', 'Bolero',
   'Fortuner', 'KWID', 'Amaze', 'Santro', 'XUV500', 'KUV100', 'Ignis',
   'RediGO', 'Scorpio', 'Marazzo', 'Aspire', 'Figo', 'Vitara',
   'Tiago', 'Polo', 'Seltos', 'Celerio', 'GO', '5', 'CR-V',
   'Endeavour', 'KUV', 'Jazz', '3', 'A4', 'Tigor', 'Ertiga', 'Safari',
   'Thar', 'Hexa', 'Rover', 'Eeco', 'A6', 'E-Class', 'Q7', 'Z4', '6',
   'XF', 'X5', 'Hector', 'Civic', 'D-Max', 'Cayenne', 'X1', 'Rapid',
   'Freestyle', 'Superb', 'Nexon', 'XUV300', 'Dzire VXI', 'S90',
   'WR-V', 'XL6', 'Triber', 'ES', 'Wrangler', 'Camry', 'Elantra',
   'Yaris', 'GL-Class', '7', 'S-Presso', 'Dzire LXI', 'Aura', 'XC',
   'Ghibli', 'Continental', 'CR', 'Kicks', 'S-Class', 'Tucson',
   'Harrier', 'X3', 'Octavia', 'Compass', 'CLS', 'redi-GO', 'Glanza',
   'Macan', 'X4', 'Dzire ZXI', 'XC90', 'F-PACE', 'A8', 'MUX',
   'GTC4Lusso', 'GLS', 'X-Trail', 'XE', 'XC60', 'Panamera', 'Alturas',
   'Altroz', 'NX', 'Carnival', 'C', 'RX', 'Ghost', 'Quattroporte',
   'Gurkha']

# Input form
with st.form("car_input_form"):
    col1, col2 = st.columns(2)

    with col1:
        model_input = st.selectbox("Car Model", model_list)
        age = st.number_input("Vehicle Age (years)", min_value=0, max_value=30, step=1)
        km = st.number_input("Kilometers Driven", min_value=0, step=100)
        seller = st.selectbox("Seller Type", ['Individual','Dealer', 'Trustmark Dealer'])
        fuel = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric'])

    with col2:
        transmission = st.selectbox("Transmission Type", ['Manual', 'Automatic'])
        mileage = st.number_input("Mileage (km/l)", min_value=0.0, step=0.1)
        engine = st.number_input("Engine Size (CC)", min_value=500, max_value=5000, step=10)
        seats = st.slider("Number of Seats", 2, 10, 1)

    submit = st.form_submit_button("Predict Price")

# 🔍 Prediction Logic
if submit:
    # Encode categorical inputs
    seller_map = {'Individual': 1, 'Dealer': 2, 'Trustmark Dealer': 3}
    fuel_map = {'Petrol': 1, 'Diesel': 2, 'CNG': 3, 'LPG': 4, 'Electric': 5}
    transmission_map = {'Manual': 1, 'Automatic': 2}

    seller = seller_map[seller]
    fuel = fuel_map[fuel]
    transmission = transmission_map[transmission]
    model_input_encoded = model_list.index(model_input) + 1

    input_df = pd.DataFrame([[model_input_encoded, age, km, seller, fuel, transmission, mileage, engine, seats]],
                            columns=['model', 'vehicle_age', 'km_driven', 'seller_type',
                                     'fuel_type', 'transmission_type', 'mileage', 'engine', 'seats'])

    try:
        prediction = model.predict(input_df)[0]
        st.success(f"💰 Estimated Selling Price: ₹ {int(prediction):,}")
    except Exception as e:
        st.error("⚠️ Something went wrong during prediction.")
        st.exception(e)

# 🚪 Logout button
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
