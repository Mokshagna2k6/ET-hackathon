import streamlit as st
import sqlite3
import pandas as pd
import os
from google import genai
from components.sidebar import render_global_sidebar
from dotenv import load_dotenv

# --- PAGE SETUP ---
st.set_page_config(page_title="ET Wealth Mentor", page_icon="📈", layout="wide")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=api_key)

# --- DATABASE FETCHING & PATH FIX ---
# We use multiple possible paths to ensure it finds the DB no matter where Streamlit is run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
possible_paths = [
    os.path.join(BASE_DIR, "data", "transactions.db"),           # Matches your screenshot
    os.path.join(BASE_DIR, "backend", "data", "transactions.db") # Fallback
]
DB_PATH = next((p for p in possible_paths if os.path.exists(p)), possible_paths[0])

@st.cache_data(ttl=60)
def load_financial_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

# --- REAL-WORLD FINANCIAL LOGIC ---
total_spend, black_hole_sum, black_hole_count, ecom_spend, food_spend = 0, 0, 0, 0, 0
health_score = 100
# For hackathon demo purposes, we assume a standard entry-level monthly income of ₹60,000
ASSUMED_INCOME = 60000 

df = load_financial_data()

if not df.empty:
    try:
        total_spend = df["amount"].sum()
        
        # Micro-transactions
        micro_txns = df[df['amount'] < 300]
        black_hole_sum = micro_txns['amount'].sum()
        black_hole_count = len(micro_txns)
        
        # Categorical Spend
        ecom_spend = df[df['category'] == 'Shopping / E-commerce']['amount'].sum()
        food_spend = df[df['category'] == 'Food & Dining']['amount'].sum()
        
        # Advanced Health Score Algorithm (Based on 50/30/20 Rule)
        discretionary_spend = ecom_spend + food_spend
        discretionary_ratio = discretionary_spend / ASSUMED_INCOME
        
        # Penalty 1: If discretionary spending is > 30% of income
        if discretionary_ratio > 0.3:
            health_score -= int((discretionary_ratio - 0.3) * 100)
            
        # Penalty 2: High UPI Black Hole (Wasted micro-spends)
        if black_hole_sum > (ASSUMED_INCOME * 0.1): # If they waste > 10% on micro-txns
            health_score -= 15
            
        # Penalty 3: Spending more than income
        if total_spend > ASSUMED_INCOME:
            health_score -= 40
            
        health_score = max(10, min(100, health_score)) # Ensure score stays between 10 and 100
        
    except Exception as e:
        st.warning(f"Data formatting error: {e}")
else:
    st.error(f"⚠️ Database is empty. Could not find data at: {DB_PATH}. Please run seed_db.py first!")

# --- UI RENDERING ---
st.markdown("""
    <style>
    .et-header { color: #D32F2F; font-weight: bold; font-size: 2.5rem; }
    .mentor-alert { border-left: 4px solid #D32F2F; padding-left: 15px; background-color: rgba(211, 47, 47, 0.1); border-radius: 5px; margin-bottom: 15px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="et-header">📈 ET Wealth Mentor </div>', unsafe_allow_html=True)
st.markdown("Your autonomous financial advisor, powered by your real-time banking data.")
st.divider()

st.subheader("🏥 Financial Health Diagnostics")
col1, col2, col3 = st.columns(3)

col1.metric(label="Money Health Score", value=f"{health_score} / 100", delta="Based on 50/30/20 Rule" if total_spend > 0 else "", delta_color="normal")
col2.metric(label="UPI Black Hole (< ₹300 txns)", value=f"₹{black_hole_sum:,.2f}", delta=f"{black_hole_count} micro-transactions", delta_color="inverse")
col3.metric(label="Total Processed Spend", value=f"₹{total_spend:,.2f}", delta=f"Budget: ₹{ASSUMED_INCOME:,.2f}")

st.divider()

st.subheader("🚨 Mentor Insights & Interventions")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="mentor-alert">', unsafe_allow_html=True)
    st.markdown("#### 🛍️ Lifestyle Creep Detected")
    st.write(f"**Trigger:** You have spent **₹{ecom_spend:,.2f}** on E-commerce.")
    st.write("**Action Plan:** Institute a 48-hour cool-down rule for online purchases over ₹2,000 to protect your emergency fund.")
    st.button("Enable Purchase Alerts", key="btn_creep")
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="mentor-alert" style="border-left-color: #2E7D32; background-color: rgba(46, 125, 50, 0.1);">', unsafe_allow_html=True)
    st.markdown("#### 🌉 ET Wealth Bridge: Food to Funds")
    st.write(f"**Trigger:** You spent **₹{food_spend:,.2f}** on Food & Dining.")
    st.write(f"**Recommendation:** The Nifty India Consumption Index is up 14%. Divert 20% of your food budget (**₹{food_spend * 0.2:,.2f}**) into a Consumption SIP.")
    st.button("Explore ET Mutual Funds", key="btn_wealth")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- RAG CHATBOT (Upgraded Prompt) ---
st.subheader("💬 Ask Your Mentor")
st.markdown("Type any financial question or ask for personalized advice based on your transaction history.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your ET Wealth Mentor. I have securely analyzed your recent transactions. What would you like to know?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g., Can I afford a ₹50,000 PS5 this month?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your financial data and generating insights..."):
            try:
                # REFINED LLM PROMPT
                financial_summary = f"""
                You are the 'ET Wealth Mentor', an elite, AI-powered financial advisor built by The Economic Times.
                Your goal is to turn confused savers into confident investors.
                
                USER FINANCIAL DATA (Current Month):
                - Assumed Monthly Income: ₹{ASSUMED_INCOME}
                - Total Spent: ₹{total_spend}
                - Discretionary Spend (Food + E-com): ₹{discretionary_spend}
                - 'UPI Black Hole' (Money wasted on <₹300 micro-transactions): ₹{black_hole_sum}
                - Money Health Score: {health_score}/100
                
                USER QUERY: "{prompt}"
                
                INSTRUCTIONS:
                1. Be direct, highly professional, and empathetic. Do not use generic filler.
                2. Base your math ONLY on the provided User Data.
                3. If they ask about buying something, calculate if they can afford it based on (Income - Total Spent).
                4. Always try to find money they can redirect into an investment (e.g., "If you cut your UPI Black Hole in half, you can start a ₹X SIP").
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=financial_summary,
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: Ensure your API key is correct. ({e})")

try:
    render_global_sidebar()
except Exception:
    pass