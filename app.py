import streamlit as st
import pandas as pd
import joblib

# 1. Load the model
model = joblib.load('rf_house_price_model.pkl')

st.title("🏡 House Price Prediction App")

# 2. Define inputs (matching training feature names exactly)
col1, col2 = st.columns(2)

with col1:
    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)
    sqft = st.number_input("Square Feet (sqft)", min_value=500, value=2000)
    lot_size = st.number_input("Lot Size", min_value=500, value=5000)
    year_built = st.number_input("Year Built", min_value=1800, max_value=2025, value=2000)
    garage = st.number_input("Garage Spaces", min_value=0, max_value=5, value=1)

with col2:
    location = st.selectbox("Location", ["Rural", "Downtown", "Hills", "Waterfront", "Suburb"])
    house_type = st.selectbox("House Type", ["Condo", "Townhouse", "House", "Villa", "Apartment"])
    
    # FIX: Map categorical labels to the numbers used in training
    condition_label = st.selectbox("Condition", ["Poor", "Fair", "Average", "Good", "Excellent"])
    condition_map = {"Poor": 1, "Fair": 2, "Average": 3, "Good": 4, "Excellent": 5}
    condition = condition_map[condition_label]
    
    has_pool = st.selectbox("Has Pool?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    has_fireplace = st.selectbox("Has Fireplace?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    has_basement = st.selectbox("Has Basement?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    school_rating = st.slider("School Rating", 1, 10, 5)

# Calculate 'age' based on year_built (as seen in your dataset)
age = 2025 - year_built

# 3. Create DataFrame for prediction
input_data = pd.DataFrame({
    'bedrooms': [bedrooms],
    'bathrooms': [bathrooms],
    'sqft': [sqft],
    'lot_size': [lot_size],
    'age': [age],
    'year_built': [year_built],
    'garage': [garage],
    'location': [location],
    'house_type': [house_type],
    'condition': [condition], # Now a number (1-5)
    'has_pool': [has_pool],
    'has_fireplace': [has_fireplace],
    'has_basement': [has_basement],
    'school_rating': [school_rating]
})

# 4. Predict
if st.button("Predict Price"):
    prediction = model.predict(input_data)
    st.success(f"Predicted House Price: ${prediction[0]:,.2f}")