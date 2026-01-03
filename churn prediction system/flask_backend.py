from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("model/churn_model.pkl")
scaler = joblib.load("model/scaler.pkl")
feature_columns = joblib.load("model/feature_columns.pkl")

def preprocess_input(data):
    df = pd.DataFrame([data])

    yes_no_cols = [
        'Partner','Dependents','PhoneService','PaperlessBilling',
        'OnlineSecurity','OnlineBackup','DeviceProtection',
        'TechSupport','StreamingTV','StreamingMovies'
    ]
    for col in yes_no_cols:
        df[col] = df[col].map({'Yes': 1, 'No': 0})

    df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})

    contract_map = {'Month-to-month': 3, 'One year': 2, 'Two year': 1}
    df['contract_risk'] = df['Contract'].map(contract_map)

    df['payment_risk'] = df['PaymentMethod'].apply(
        lambda x: 2 if x == 'Electronic check' else 1
    )

    service_cols = [
        'OnlineSecurity','OnlineBackup','DeviceProtection',
        'TechSupport','StreamingTV','StreamingMovies'
    ]
    df['total_services'] = df[service_cols].sum(axis=1)

    df.drop(['Contract','PaymentMethod'], axis=1, inplace=True)

    df = pd.get_dummies(df)

    df = df.reindex(columns=feature_columns, fill_value=0)

    num_cols = ['tenure','MonthlyCharges','TotalCharges']
    df[num_cols] = scaler.transform(df[num_cols])

    return df

def risk_level(prob):
    if prob < 0.3:
        return "Low Risk", "No Action"
    elif prob < 0.6:
        return "Medium Risk", "Send Retention Email / Offer Discount"
    else:
        return "High Risk", "Call Retention Team / Premium Offer"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    processed = preprocess_input(data)
    prob = model.predict_proba(processed)[0][1]
    prediction = "Will Churn" if prob > 0.5 else "Will Stay"
    level, action = risk_level(prob)

    return jsonify({
        "prediction": prediction,
        "churn_probability": round(prob,2),
        "risk_level": level,
        "suggested_action": action
    })

if __name__ == "__main__":
    app.run(debug=True)
