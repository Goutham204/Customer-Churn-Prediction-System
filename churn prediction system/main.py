import streamlit as st
import requests

st.set_page_config(page_title="Customer Churn Predictor", layout="centered")
st.title("CUSTOMER CHURN PREDICTOR")

st.subheader("Customer Information")
gender = st.selectbox("Gender", ["Male", "Female"])
senior = st.selectbox("Senior Citizen", ["No", "Yes"])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["Yes", "No"])

st.subheader("Account Details")
tenure = st.number_input("Tenure (months)", 0, 100, 12)
contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
payment = st.selectbox("Payment Method", [
    "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
])

st.subheader("Services")
phone = st.selectbox("Phone Service", ["Yes", "No"])
multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No"])
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
online_sec = st.selectbox("Online Security", ["Yes", "No"])
backup = st.selectbox("Online Backup", ["Yes", "No"])
device = st.selectbox("Device Protection", ["Yes", "No"])
tech = st.selectbox("Tech Support", ["Yes", "No"])
tv = st.selectbox("Streaming TV", ["Yes", "No"])
movies = st.selectbox("Streaming Movies", ["Yes", "No"])

st.subheader("Billing")
monthly = st.number_input("Monthly Charges", 0.0, 1000.0, 89.85)
total = st.number_input("Total Charges", 0.0, 5000.0, 1257.90)

if st.button("Predict Churn"):
    payload = {
        "gender": gender,
        "SeniorCitizen": 1 if senior=="Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "PaperlessBilling": paperless,
        "Contract": contract,
        "PaymentMethod": payment,
        "OnlineSecurity": online_sec,
        "OnlineBackup": backup,
        "DeviceProtection": device,
        "TechSupport": tech,
        "StreamingTV": tv,
        "StreamingMovies": movies,
        "MonthlyCharges": monthly,
        "TotalCharges": total
    }

    response = requests.post("http://127.0.0.1:5000/predict", json=payload)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Prediction: {result['prediction']}")
        st.write(f"Churn Probability: {result['churn_probability']}")
        st.write(f"Risk Level: {result['risk_level']}")
        st.write(f"Suggested Action: {result['suggested_action']}")
    else:
        st.error("Prediction failed. Please check backend.")
