import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SuperKart Sales Forecaster", page_icon="🛒", layout="centered")

st.title("🛒 SuperKart Store Sales Prediction")
st.markdown("Predict quarterly store-level product revenue using the deployed SuperKart XGBoost API.")

# Sidebar configuration for Backend API URL (defaults to Docker network container name)
st.sidebar.header("API Configuration")
backend_url = st.sidebar.text_input("Backend API Base URL", value="http://superkart-backend:7860")

tab1, tab2 = st.tabs(["Single Product Forecast", "Batch CSV Forecast"])

with tab1:
  st.subheader("Enter Product & Store Details")

  col1, col2 = st.columns(2)
  with col1:
      product_id = st.text_input("Product ID", value="FD6114")
      product_weight = st.number_input("Product Weight", min_value=0.1, max_value=50.0, value=12.66, step=0.1)
      product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
      product_area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027, step=0.005, format="%.3f")
      product_type = st.selectbox(
          "Product Type",
          [
              "Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy",
              "Household", "Baking Goods", "Canned", "Health and Hygiene",
              "Meat", "Soft Drinks", "Breads", "Hard Drinks",
              "Others", "Starchy Foods", "Breakfast", "Seafood"
          ]
      )
      product_mrp = st.number_input("Product MRP ($)", min_value=1.0, max_value=500.0, value=117.08, step=1.0)

with col2:
    store_id = st.selectbox("Store ID", ["OUT004", "OUT001", "OUT003", "OUT002"])
    store_year = st.selectbox("Store Establishment Year", [2009, 1987, 1999, 1998])
    store_size = st.selectbox("Store Size", ["Medium", "High", "Small"])
    city_type = st.selectbox("Store Location City Type", ["Tier 2", "Tier 1", "Tier 3"])
    store_type = st.selectbox(
        "Store Type",
      ["Supermarket Type2", "Supermarket Type1", "Departmental Store", "Food Mart"]
    )

if st.button("Predict Store Sales", type="primary"):
    payload = {
        "Product_Id": product_id,
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar,
        "Product_Allocated_Area": product_area,
        "Product_Type": product_type,
        "Product_MRP": product_mrp,
        "Store_Id": store_id,
        "Store_Establishment_Year": store_year,
        "Store_Size": store_size,
        "Store_Location_City_Type": city_type,
        "Store_Type": store_type,
    }

    try:
        response = requests.post(f"{backend_url.rstrip('/')}/v1/predict", json=payload, timeout=15)
        if response.status_code == 200:
            sales_pred = response.json()["Sales"]
            st.success(f"Predicted Product Store Sales Total: **${sales_pred:,.2f}**")
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
    except Exception as e:
        st.error(f"Connection Error: {e}")

with tab2:
    st.subheader("Upload Batch CSV for Sales Prediction")
    uploaded_file = st.file_uploader("Upload CSV file containing SuperKart product/store records", type=["csv"])

    if uploaded_file is not None and st.button("Run Batch Prediction", type="primary"):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            response = requests.post(f"{backend_url.rstrip('/')}/v1/predictbatch", files=files, timeout=30)
            if response.status_code == 200:
                preds_dict = response.json()
                results_df = pd.DataFrame(list(preds_dict.items()), columns=["Product_Id", "Predicted_Sales"])
                st.success(f"Generated predictions for {len(results_df)} records!")
                st.dataframe(results_df, use_container_width=True)
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")
      except Exception as e:
          st.error(f"Connection Error: {e}")
