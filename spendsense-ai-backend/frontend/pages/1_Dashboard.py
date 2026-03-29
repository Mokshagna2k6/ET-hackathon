import streamlit as st
import sqlite3
import pandas as pd
import os
from google import genai
from components.sidebar import render_global_sidebar
from dotenv import load_dotenv
from datetime import datetime, timedelta

st.set_page_config(page_title="ET Wealth Mentor", page_icon="📈", layout="wide")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=api_key)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
FRONTEND_DIR = os.path.dirname(CURRENT_DIR)              
PROJECT_ROOT = os.path.dirname(FRONTEND_DIR)             
DB_PATH = os.path.join(PROJECT_ROOT, "data", "transactions.db")

@st.cache_data(ttl=60)
def load_financial_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

total_spend, black_hole_sum, black_hole_count = 0, 0, 0
ecom_spend, food_spend, investment_spend, discretionary_spend = 0, 0, 0, 0
health_score = 100
health_tier = "Unknown"
recent_history = "No recent transactions found."

ASSUMED_INCOME = st.session_state.get("monthly_income", 60000)
CREDIT_LIMIT = st.session_state.get("credit_limit", 100000)

df = load_financial_data()

if not df.empty:
    try:
        base_date = datetime.today()
        dates = [base_date - timedelta(days=x) for x in range(len(df))]
        dates.reverse() 
        df['transaction_date'] = [d.strftime("%Y-%m-%d") for d in dates]

       
        recent_history = df.tail(20)[['transaction_date', 'merchant_name', 'amount', 'category']].to_string(index=False)
        
        total_spend = df["amount"].sum()
        
        
        ecom_spend = df[df['category'] == 'Shopping / E-commerce']['amount'].sum()
        food_spend = df[df['category'] == 'Food & Dining']['amount'].sum()
        discretionary_spend = ecom_spend + food_spend
        
        investment_spend = df[df['category'].isin(['Financial Services', 'Investment', 'Crypto', 'Education'])]['amount'].sum()
        
      
        micro_txns = df[(df['amount'] < 300) & (df['payment_method'].str.contains('UPI', case=False, na=False))]
        black_hole_sum = micro_txns['amount'].sum()
        black_hole_count = len(micro_txns)
        
        credit_spend = df[df['amount'] > 2000]['amount'].sum() 
        
        savings_and_investments = (ASSUMED_INCOME - total_spend) + investment_spend
        savings_ratio = max(0, savings_and_investments / ASSUMED_INCOME)
        
        discretionary_ratio = discretionary_spend / ASSUMED_INCOME
        micro_spend_ratio = black_hole_sum / total_spend if total_spend > 0 else 0
        utilization_ratio = credit_spend / CREDIT_LIMIT
        
        score_fire = min(35, (savings_ratio / 0.20) * 35)
        
        if discretionary_ratio <= 0.30:
            score_disc = 30
        else:
            score_disc = max(0, 30 - ((discretionary_ratio - 0.30) / 0.30) * 30)
            
        if micro_spend_ratio <= 0.05:
            score_leak = 20
        else:
            score_leak = max(0, 20 - ((micro_spend_ratio - 0.05) / 0.15) * 20)
            
        if utilization_ratio <= 0.30:
            score_credit = 15
        else:
            score_credit = max(0, 15 - ((utilization_ratio - 0.30) / 0.40) * 15)
            
        health_score = int(score_fire + score_disc + score_leak + score_credit)
        health_score = max(10, min(100, health_score)) 
        
        if health_score >= 80:
            health_tier = "Wealth Builder 🟢"
        elif health_score >= 60:
            health_tier = "Stable, but Leaking 🟡"
        elif health_score >= 40:
            health_tier = "Living Paycheck to Paycheck 🟠"
        else:
            health_tier = "High Financial Risk 🔴"
        
    except Exception as e:
        st.warning(f"Data calculation error: {e}")

st.markdown("""
    <style>
    .et-header { color: #D32F2F; font-weight: bold; font-size: 2.5rem; }
    .mentor-alert { border-left: 4px solid #D32F2F; padding-left: 15px; background-color: rgba(211, 47, 47, 0.1); border-radius: 5px; margin-bottom: 15px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="et-header">📈 ET Wealth Mentor </div>', unsafe_allow_html=True)
st.markdown("Your autonomous financial advisor, powered by your real-time banking data.")
st.divider()

col_refresh, col_empty = st.columns([1, 3])
with col_refresh:
    if st.button("🔄 Force Sync with Database", type="secondary"):
        st.cache_data.clear()
        st.rerun()

if df.empty:
    st.error(f"⚠️ Debug: Database missing or empty at '{DB_PATH}'. Please run seed_db.py")
else:
    st.success(f"✅ Debug: Loaded {len(df)} transactions from '{DB_PATH}'")
    
st.divider()

st.subheader("🏥 Financial Health Diagnostics")
col1, col2, col3 = st.columns(3)

col1.metric(label="Money Health Score", value=f"{health_score} / 100", delta=health_tier, delta_color="normal")
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
    
    if st.button("Enable Purchase Alerts", key="btn_creep"):
        st.toast("✅ SMS & WhatsApp Alerts Enabled!", icon="🔔")
        st.success("Alerts active! The Mentor will notify you on your next >₹2,000 purchase.")
        
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="mentor-alert" style="border-left-color: #2E7D32; background-color: rgba(46, 125, 50, 0.1);">', unsafe_allow_html=True)
    st.markdown("#### 🌉 ET Wealth Bridge: Food to Funds")
    st.write(f"**Trigger:** You spent **₹{food_spend:,.2f}** on Food & Dining.")
    st.write(f"**Recommendation:** The Nifty India Consumption Index is up 14%. Divert 20% of your food budget (**₹{food_spend * 0.2:,.2f}**) into a Consumption SIP.")
    
    if st.button("Explore ET Mutual Funds", key="btn_wealth"):
        st.toast("Redirecting to ET Money...", icon="🚀")
        st.balloons() 
        st.success(f"🎉 Success! Mock Auto-SIP of ₹{food_spend * 0.2:,.2f}/month initiated via ET Wealth Bridge.")
        
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.subheader("💬 Ask Your Mentor")
st.markdown("Type any financial question or ask for personalized advice based on your transaction history.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your strict but highly effective ET Wealth Mentor. I have analyzed your 4-Pillar Financial Index. What would you like to plan today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g., What are my transactions for the past 3 days in a tabular format?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your financial data and generating insights..."):
            try:
                financial_summary = f"""
                You are the 'ET Wealth Mentor', an elite, AI-powered financial advisor built by The Economic Times.
                Your tone is highly professional, data-driven, slightly strict, but ultimately encouraging. 
                Your goal is to turn confused savers into confident investors by utilizing the 4-Pillar Wealth Index.
                
                USER FINANCIAL DATA (Current Month):
                - Assumed Monthly Income: ₹{ASSUMED_INCOME}
                - Total Spent: ₹{total_spend}
                - Active Investments: ₹{investment_spend}
                - Discretionary Spend (Food + E-com): ₹{discretionary_spend}
                - 'UPI Black Hole' (Money wasted on <₹300 micro-transactions): ₹{black_hole_sum}
                
                WEALTH INDEX METRICS:
                - Overall Health Score: {health_score}/100 
                - Health Tier: {health_tier}
                
                RECENT TRANSACTION HISTORY (Last 20 transactions):
                {recent_history}
                
                USER QUERY: "{prompt}"
                
                INSTRUCTIONS:
                1. Answer directly based ONLY on this exact data. Do not use generic financial advice.
                2. Be strict about the 'UPI Black Hole' and Discretionary spending if it is high.
                3. Always map spending habits back to investing. If they want to buy something, tell them how to afford it by cutting specific waste.
                4. If the user asks for their recent transactions, read the 'RECENT TRANSACTION HISTORY' provided above and format it beautifully into a Markdown table for them.
                5. Keep the response concise, punchy, and structured with bullet points where appropriate.
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