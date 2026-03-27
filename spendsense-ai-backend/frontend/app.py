import streamlit as st
import requests
from components.sidebar import render_global_sidebar

# --- PAGE CONFIGURATION ---
# Must be the very first Streamlit command
st.set_page_config(
    page_title="SpendSense AI",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HEADER ---
st.title("💸 SpendSense AI")
st.markdown("### Agentic Merchant Resolution Engine (AMRE)")
st.write("Welcome to the command center. Use the sidebar to navigate to the Dashboard or Process Transactions.")
st.divider()

# --- BACKEND CONNECTION TEST ---
st.subheader("📡 System Status")

try: 
    # Attempt to ping the FastAPI health endpoint
    response = requests.get("http://127.0.0.1:8000/")
    
    if response.status_code == 200:
        st.success(f"✅ Backend Connected: {response.json().get('status', 'OK')}")
    else:
        st.warning(f"⚠️ Backend returned unexpected code: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    st.error("🚨 CRITICAL: Cannot connect to the FastAPI backend!")
    st.info("💡 Fix: Ensure you have a separate terminal running `uvicorn backend.app.main:app --reload`")

render_global_sidebar()

