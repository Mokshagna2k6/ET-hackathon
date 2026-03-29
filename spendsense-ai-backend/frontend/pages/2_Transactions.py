import streamlit as st
import sqlite3
import pandas as pd
import requests
import os
from components.sidebar import render_global_sidebar


st.set_page_config(page_title="Transactions Hub", page_icon="💳", layout="wide")


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
FRONTEND_DIR = os.path.dirname(CURRENT_DIR)              
PROJECT_ROOT = os.path.dirname(FRONTEND_DIR)             
DB_PATH = os.path.join(PROJECT_ROOT, "data", "transactions.db")

@st.cache_data(ttl=30)
def load_all_transactions():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    
    df = pd.read_sql_query("SELECT * FROM transactions ORDER BY id DESC", conn)
    conn.close()
    return df

st.markdown('<div style="color: #D32F2F; font-weight: bold; font-size: 2.5rem;">💳 Transactions Hub</div>', unsafe_allow_html=True)
st.markdown("Process new SMS messages or view your entire transaction ledger.")

tab1, tab2 = st.tabs(["📥 Process New SMS", "🗄️ Transaction Ledger"])


with tab1:
    st.subheader("Process Bank SMS")
    st.markdown("Paste a raw bank SMS below. AMRE will extract the data and research the merchant.")

    sms_input = st.text_area(
        "Raw SMS Text",
        height=100,
        placeholder="e.g., Rs 240.00 debited from a/c **1234 on 05-03-26 to VPA-qwikcilver@hdfcbank. Ref: 4321"
    )

    if st.button("🔍 Analyze Transaction", type="primary"):
        if not sms_input.strip():
            st.warning("⚠️ Please paste an SMS message first.")
        else:
            with st.spinner("🕵️‍♂️ AMRE is investigating the merchant..."):
                try:
                    payload = {"sms_text": sms_input}
                    response = requests.post("http://127.0.0.1:8000/api/v1/process-sms", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ Analysis Complete! The transaction has been saved to the database.")
                        
                        st.divider()
                        st.subheader("🧾 Enriched Profile")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Amount", f"₹{data['transaction']['amount']}")
                        col2.metric("Payment Method", data['transaction']['payment_method'])
                        col3.metric("Confidence Score", f"{int(data['confidence_score'] * 100)}%")
                        
                        st.markdown("### 🏢 Merchant Details")
                        st.write(f"**Real Brand Name:** {data['transaction']['merchant_name']}")
                        st.write(f"**Business Category:** {data['category']}")
                        st.write(f"**Raw ID Tracked:** `{data['transaction']['raw_upi_id']}`")
                        
                        if data['is_suspicious']:
                            st.error("🚨 WARNING: This merchant has been flagged as suspicious or unknown!")
                        else:
                            st.info("🛡️ Merchant verified as safe.")
                            
                        with st.expander("💻 View Raw JSON Data"):
                            st.json(data)
                            
                    else:
                        st.error(f"Backend Error: {response.status_code}")
                        st.write(response.text)
                        
                except requests.exceptions.ConnectionError:
                    st.error("🚨 Cannot connect to the backend. Is your FastAPI server running?")


with tab2:
    st.subheader("Transaction Ledger")
    
   
    if st.button("🔄 Refresh Ledger Data"):
        st.cache_data.clear()
        
    df = load_all_transactions()
    
    if not df.empty:
       
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            category_filter = st.selectbox("Filter by Category", ["All Categories"] + list(df['category'].unique()))
        with col_f2:
            search_merchant = st.text_input("Search Merchant (e.g., Zomato, Amazon)")

        
        filtered_df = df.copy()
        if category_filter != "All Categories":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
        if search_merchant:
            filtered_df = filtered_df[filtered_df['merchant_name'].str.contains(search_merchant, case=False, na=False)]

        st.markdown(f"**Showing {len(filtered_df)} transactions | Total Spend in view: ₹{filtered_df['amount'].sum():,.2f}**")

        st.dataframe(
            filtered_df[['id', 'merchant_name', 'amount', 'category', 'payment_method', 'confidence_score']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("Txn ID", format="%d"),
                "merchant_name": st.column_config.TextColumn("Merchant / Brand"),
                "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                "category": st.column_config.TextColumn("Category"),
                "payment_method": st.column_config.TextColumn("Method"),
                "confidence_score": st.column_config.ProgressColumn(
                    "AI Confidence",
                    help="The Sherlock Agent's confidence in resolving the brand name.",
                    format="%.2f",
                    min_value=0,
                    max_value=1,
                ),
            }
        )
    else:
        st.info("No transactions found in the database. Process an SMS in the first tab to populate this ledger.")

try:
    render_global_sidebar()
except Exception:
    pass