# Import necessary libraries
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application
superkart_api = Flask("SuperKart Sales Predictor")

# Load the trained SuperKart model pipeline
model = joblib.load("superkart_model.joblib")

def prepare_features(df):
"""Apply the exact preprocessing/feature engineering transformations expected by the pipeline."""
df = df.copy()
if "Product_Sugar_Content" in df.columns:
df["Product_Sugar_Content"] = df["Product_Sugar_Content"].replace({"reg": "Regular"})
if "Store_Establishment_Year" in df.columns and "Store_Age" not in df.columns:
df["Store_Age"] = 2026 - df["Store_Establishment_Year"]
if "Product_Id" in df.columns and "Product_Id_Prefix" not in df.columns:
df["Product_Id_Prefix"] = df["Product_Id"].astype(str).str[:2]
return df

# Define a route for the home page (health check)
@superkart_api.get("/")
def home():
return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint for single (online) prediction
@superkart_api.post("/v1/predict")
def predict_sales():
# Get JSON data from the request
data = request.get_json()

# Convert JSON payload to a single-row DataFrame
sample = pd.DataFrame([data])
sample = prepare_features(sample)

# Make prediction
prediction = model.predict(sample).tolist()[0]

# Return the prediction as JSON
return jsonify({"Sales": round(float(prediction), 2)})

# Define an endpoint for batch prediction
@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
# Get uploaded CSV file from the request
file = request.files["file"]

# Read CSV into a DataFrame
input_data = pd.read_csv(file)
processed_data = prepare_features(input_data)

# Make batch predictions
predictions = model.predict(processed_data).tolist()

# Map predictions to Product_Id if present, otherwise row index
if "Product_Id" in input_data.columns:
result = dict(zip(input_data["Product_Id"], [round(float(p), 2) for p in predictions]))
else:
result = {idx: round(float(p), 2) for idx, p in enumerate(predictions)}

return jsonify(result)

# Run the Flask app on port 7860
if __name__ == "__main__":
superkart_api.run(host="0.0.0.0", port=7860, debug=True)
