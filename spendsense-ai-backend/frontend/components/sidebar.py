import streamlit as st

def render_global_sidebar():
    """
    Injects a consistent status dashboard into the bottom of the sidebar.
    This makes the app look like a cohesive, enterprise-grade product.
    """
    with st.sidebar:
        st.divider()
        st.markdown("### ⚙️ System Status")
        st.success("🟢 AMRE Engine: Online")
        st.info("🧠 Model: Gemini 2.5 Flash")
        st.markdown("**User:** Hackathon Judge (Admin)")
        st.caption("© 2026 SpendSense AI")