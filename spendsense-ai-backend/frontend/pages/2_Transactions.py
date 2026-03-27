import streamlit as st
import requests

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Process Transaction", page_icon="💳", layout="centered")

st.title("💳 Process Bank SMS")
st.markdown("Paste a raw bank SMS below. AMRE will extract the data and research the merchant.")

# --- 2. THE INPUT FORM ---
sms_input = st.text_area(
    "Raw SMS Text",
    height=100,
    placeholder="e.g., Rs 240.00 debited from a/c **1234 on 05-03-26 to VPA-qwikcilver@hdfcbank. Ref: 4321"
)

# --- 3. THE ACTION BUTTON ---
# type="primary" makes the button stand out
if st.button("🔍 Analyze Transaction", type="primary"):
    
    # Check if the user actually typed something
    if not sms_input.strip():
        st.warning("⚠️ Please paste an SMS message first.")
    else:
        # Show a loading spinner while the AI thinks
        with st.spinner("🕵️‍♂️ AMRE is investigating the merchant..."):
            try:
                # --- 4. CALL THE BACKEND API ---
                # We format the data exactly how our FastAPI server expects it
                payload = {"sms_text": sms_input}
                response = requests.post("http://127.0.0.1:8000/api/v1/process-sms", json=payload)
                
                # --- 5. DISPLAY THE RESULTS ---
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Analysis Complete!")
                    
                    st.divider()
                    st.subheader("🧾 Enriched Profile")
                    
                    # Create 3 neat columns for key metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Amount", f"₹{data['transaction']['amount']}")
                    col2.metric("Payment Method", data['transaction']['payment_method'])
                    col3.metric("Confidence Score", f"{int(data['confidence_score'] * 100)}%")
                    
                    # Display the researched merchant info
                    st.markdown("### 🏢 Merchant Details")
                    st.write(f"**Real Brand Name:** {data['transaction']['merchant_name']}")
                    st.write(f"**Business Category:** {data['category']}")
                    st.write(f"**Raw ID Tracked:** `{data['transaction']['raw_upi_id']}`")
                    
                    # Security Flagging
                    if data['is_suspicious']:
                        st.error("🚨 WARNING: This merchant has been flagged as suspicious or unknown!")
                    else:
                        st.info("🛡️ Merchant verified as safe.")
                        
                    # A dropdown for the judges to see the raw JSON
                    with st.expander("💻 View Raw JSON Data"):
                        st.json(data)
                        
                else:
                    st.error(f"Backend Error: {response.status_code}")
                    st.write(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Cannot connect to the backend. Is your FastAPI server running?")