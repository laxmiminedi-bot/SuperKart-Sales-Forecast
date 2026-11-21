import joblib
import pandas as pd
from flask import Flask, request, jsonify

superkart_api = Flask("SuperKart Sales Predictor")
model = joblib.load("superkart_model.joblib")

def prepare_features(df):
    df = df.copy()
    if "Product_Sugar_Content" in df.columns:
        df["Product_Sugar_Content"] = df["Product_Sugar_Content"].replace({"reg": "Regular"})
    if "Store_Establishment_Year" in df.columns and "Store_Age" not in df.columns:
        df["Store_Age"] = 2026 - df["Store_Establishment_Year"]
    if "Product_Id" in df.columns and "Product_Id_Prefix" not in df.columns:
        df["Product_Id_Prefix"] = df["Product_Id"].astype(str).str[:2]
    return df

@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

@superkart_api.post("/v1/predict")
def predict_sales():
    data = request.get_json()
    sample = prepare_features(pd.DataFrame([data]))
    prediction = model.predict(sample).tolist()[0]
    return jsonify({"Sales": round(float(prediction), 2)})

@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    file = request.files["file"]
    input_data = pd.read_csv(file)
    processed_data = prepare_features(input_data)
    predictions = model.predict(processed_data).tolist()
    if "Product_Id" in input_data.columns:
        result = dict(zip(input_data["Product_Id"], [round(float(p), 2) for p in predictions]))
    else:
        result = {idx: round(float(p), 2) for idx, p in enumerate(predictions)}
    return jsonify(result)

if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860, debug=True)
