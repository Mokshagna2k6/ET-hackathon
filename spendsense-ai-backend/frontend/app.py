import streamlit as st
import requests
import sqlite3
import pandas as pd
import os
from components.sidebar import render_global_sidebar


st.set_page_config(
    page_title="ET Wealth Mentor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Gradient Hero Text */
    .hero-text {
        background: -webkit-linear-gradient(45deg, #D32F2F, #FF5252);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    /* Subtitle styling */
    .sub-text {
        font-size: 1.2rem;
        color: #B0BEC5;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    /* Feature Card styling */
    .feature-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #D32F2F;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        height: 150px;
    }
    </style>
""", unsafe_allow_html=True)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)              
DB_PATH = os.path.join(PROJECT_ROOT, "data", "transactions.db")

@st.cache_data(ttl=30)
def get_global_stats():
    if not os.path.exists(DB_PATH):
        return 0, 0, 0
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT amount, raw_upi_id FROM transactions", conn)
        conn.close()
        total_volume = df['amount'].sum()
        total_txns = len(df)
        unique_merchants = df['raw_upi_id'].nunique()
        return total_volume, total_txns, unique_merchants
    except:
        return 0, 0, 0

vol, txns, merch = get_global_stats()

st.markdown('<div class="hero-text">🚀 ET Wealth Mentor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Agentic Merchant Resolution Engine (AMRE) Command Center</div>', unsafe_allow_html=True)

st.subheader("📊 AMRE Pipeline Status")
m1, m2, m3 = st.columns(3)
m1.metric("Total Capital Tracked", f"₹{vol:,.2f}")
m2.metric("Transactions Ingested", f"{txns}")
m3.metric("Unique Merchants Resolved", f"{merch}")

st.divider()

st.subheader("⚡ Quick Launch")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📈 The Dashboard</h3>
        <p>View the 4-Pillar Wealth Index, analyze the UPI Black Hole, and chat with the AI Mentor.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("") # Spacer
    if st.button("Launch Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Dashboard.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📥 Process SMS</h3>
        <p>Test the Extractor & Sherlock Agents live. Paste cryptic bank SMS messages for autonomous enrichment.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Launch Transactions Hub", use_container_width=True):
        st.switch_page("pages/2_Transactions.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🗺️ Merchant Map</h3>
        <p>View the geospatial distribution and AI confidence scores of all successfully resolved entities.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Launch Merchant Directory", use_container_width=True):
        st.switch_page("pages/3_Merchant_Map.py")

st.divider()

st.subheader("📡 System Diagnostics")

try: 
    response = requests.get("http://127.0.0.1:8000/")
    
    if response.status_code == 200:
        st.success(f"✅ Backend Connected: AMRE Orchestration Server is online and listening! ({response.json().get('status', 'OK')})")
    else:
        st.warning(f"⚠️ Backend returned unexpected code: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    st.error("🚨 CRITICAL: Cannot connect to the FastAPI backend!")
    st.info("💡 Fix: Ensure you have a separate terminal running `uvicorn backend.app.main:app --reload`")


try:
    render_global_sidebar()
except Exception:
    pass