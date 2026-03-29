import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os
from components.sidebar import render_global_sidebar

st.set_page_config(page_title="Merchant Map", page_icon="🗺️", layout="wide")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
FRONTEND_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(FRONTEND_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "data", "transactions.db")

@st.cache_data(ttl=60)
def load_merchant_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT 
            raw_upi_id as 'Raw Cryptic ID',
            merchant_name as 'Resolved Brand Name',
            category as 'Category',
            COUNT(id) as 'Total Transactions',
            SUM(amount) as 'Total Volume (₹)',
            AVG(confidence_score) as 'Avg AI Confidence'
        FROM transactions
        GROUP BY raw_upi_id, merchant_name, category
        ORDER BY 'Total Volume (₹)' DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_merchant_data()

st.markdown("""
    <style>
    .et-header { color: #D32F2F; font-weight: bold; font-size: 2.5rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="et-header">🗺️ Resolved Merchant Directory</div>', unsafe_allow_html=True)
st.markdown("A centralized view of all cryptic UPI IDs and merchants successfully resolved by the Sherlock Agent.")

if st.button("🔄 Sync Directory with Database"):
    st.cache_data.clear()
    st.rerun()

st.divider()

if not df.empty:

    st.subheader("🗂️ Known Entity Database")
    st.markdown(f"The AI has successfully resolved **{len(df)} unique merchants** from your transaction history.")

    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Raw Cryptic ID": st.column_config.TextColumn("Raw Cryptic ID"),
            "Resolved Brand Name": st.column_config.TextColumn("Resolved Brand Name", width="medium"),
            "Category": st.column_config.TextColumn("Category"),
            "Total Transactions": st.column_config.NumberColumn("Txn Count", format="%d"),
            "Total Volume (₹)": st.column_config.NumberColumn("Total Volume (₹)", format="₹%.2f"),
            "Avg AI Confidence": st.column_config.ProgressColumn(
                "Avg AI Confidence",
                help="The average confidence score from the Sherlock Agent.",
                format="%.2f",
                min_value=0,
                max_value=1,
            ),
        }
    )

    st.divider()

    st.subheader("📍 Transaction Hotspots")
    st.markdown("Geographic distribution of identified merchant terminals based on total transaction volume.")

    np.random.seed(42) 
    
    total_txns = df['Total Transactions'].sum()
   
    map_data = pd.DataFrame(
        np.random.randn(int(total_txns), 2) / [8, 8] + [22.0, 79.0],
        columns=['lat', 'lon']
    )

    st.map(map_data, color="#D32F2F") 
    st.info("💡 **Demo Note:** In a production banking environment, these plotted coordinates would be pulled directly from enriched API metadata (e.g., MCC or Terminal ID).")

else:
    st.warning("⚠️ No merchant data found. Please run the seeder or process an SMS to populate the directory.")

try:
    render_global_sidebar()
except Exception:
    pass