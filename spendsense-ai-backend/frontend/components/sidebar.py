import streamlit as st

def render_global_sidebar():
    """
    Injects a consistent status dashboard and user controls into the bottom of the sidebar.
    This makes the app look like a cohesive, enterprise-grade product.
    """
    with st.sidebar:
        st.markdown("### ⚙️ Financial Profile")
        st.markdown("Set your baseline metrics to calibrate the AMRE scoring engine.")
        
        if "monthly_income" not in st.session_state:
            st.session_state.monthly_income = 60000
        if "credit_limit" not in st.session_state:
            st.session_state.credit_limit = 100000
            
        new_income = st.number_input(
            "Monthly Income (₹)", 
            min_value=10000, 
            max_value=1000000, 
            value=st.session_state.monthly_income,
            step=5000
        )
        
        new_credit = st.number_input(
            "Total Credit Limit (₹)", 
            min_value=10000, 
            max_value=1000000, 
            value=st.session_state.credit_limit,
            step=10000
        )
        
        st.session_state.monthly_income = new_income
        st.session_state.credit_limit = new_credit
        
        st.divider()

        st.markdown("### 📡 System Status")
        st.success("🟢 AMRE Engine: Online")
        st.info("🧠 Model: Gemini 2.5 Flash")
        st.markdown("**User:** Hackathon Judge (Admin)")
        st.caption("© 2026 SpendSense AI")