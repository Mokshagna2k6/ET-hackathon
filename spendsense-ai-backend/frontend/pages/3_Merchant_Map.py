import streamlit as st
import pandas as pd
import numpy as np

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Merchant Map", page_icon="🗺️", layout="wide")

st.title("🗺️ Resolved Merchant Directory")
st.markdown("A centralized view of all cryptic UPI IDs and merchants successfully resolved by AMRE.")
st.divider()

# --- 2. INTERACTIVE DATA TABLE ---
st.subheader("🗂️ Known Entity Database")
st.markdown("Search and filter through the merchants the AI has investigated.")

# Creating a mock dataset using Pandas (Simulating your database)
data = {
    "Raw Cryptic ID": ["qwikcilver@hdfc", "fashnear@yesbank", "paytmqr2810@paytm", "bharatpe.90@icici", "razorpay@sbi"],
    "Resolved Brand Name": ["Qwikcilver (Pine Labs)", "Meesho", "Raju Tea Stall", "Local Grocery", "Razorpay Subscriptions"],
    "Category": ["Financial Services", "E-commerce", "Food & Dining", "Groceries", "Software/SaaS"],
    "Risk Level": ["Safe", "Safe", "Safe", "Medium", "Safe"],
    "AI Confidence": ["98%", "95%", "88%", "75%", "99%"]
}
df = pd.DataFrame(data)

# st.dataframe creates a beautiful, sortable UI table
st.dataframe(df, width="stretch", hide_index=True)

st.divider()

# --- 3. GEOSPATIAL MAP ---
st.subheader("📍 Transaction Hotspots")
st.markdown("Geographic distribution of identified merchant terminals (Demo Data).")

# Generating mock GPS coordinates (Latitude/Longitude) for the map
# We center these roughly over India [22.0, 79.0]
map_data = pd.DataFrame(
    np.random.randn(50, 2) / [20, 20] + [22.0, 79.0],
    columns=['lat', 'lon']
)

# st.map instantly plots these coordinates on an interactive dark-mode map!
st.map(map_data)

st.info("💡 **Demo Note:** In production, GPS coordinates would be pulled from enriched API metadata or terminal IDs.")