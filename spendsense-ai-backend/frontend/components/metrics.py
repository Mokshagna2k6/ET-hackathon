import streamlit as st

def render_kpi_row(total_spend, transactions, resolved, flags):
    """
    Renders a standardized row of 4 Key Performance Indicators (KPIs).
    """
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(label="Total Processed Spend", value=f"₹{total_spend:,}", delta="+12% vs last month")
    col2.metric(label="Transactions Analyzed", value=f"{transactions}", delta="100% automated")
    col3.metric(label="Cryptic IDs Resolved", value=f"{resolved}", delta="Saved 4 hrs of manual work")
    col4.metric(label="Suspicious Flags 🚨", value=f"{flags}", delta="-1 vs last month", delta_color="inverse")