# 💸 SpendSense AI: Agentic Merchant Resolution Engine (AMRE)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini_2.5_Flash-8E75B2?style=flat&logo=googlebard&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

**SpendSense AI** is an autonomous financial intelligence platform built to solve the "UPI Blindness" epidemic. By utilizing a multi-agent AI architecture, it transforms cryptic, unreadable bank SMS alerts into actionable wealth-building strategies.

---

## 🚨 The Problem: "UPI Blindness"
India’s UPI revolution made payments frictionless, but it destroyed financial visibility. Every day, users make dozens of micro-transactions, resulting in bank statements filled with cryptic, unreadable IDs (e.g., `VPA-fashnear@yesbank` or `qwikcilver@hdfc`). 
**You cannot budget what you cannot understand.** Existing expense trackers rely on static databases that constantly fail to identify new, local, or hyper-specific merchants.

## 🚀 The Solution: AMRE
We built the **Agentic Merchant Resolution Engine (AMRE)**. Instead of static mapping, AMRE uses a decoupled, multi-agent AI pipeline powered by Google Gemini 2.5 Flash:
1. **The Extractor Agent:** Parses messy, unstructured SMS text into clean JSON variables (Amount, Date, Ref No).
2. **The Sherlock Agent:** Dynamically investigates the cryptic UPI ID, searches for context, and resolves it to the actual real-world brand (e.g., resolving `fashnear` to **Meesho**). It assigns an AI confidence score, categorizes the business, and flags suspicious entities.

---

## ✨ Core Features & Business Logic

### 1. The ET Wealth Mentor Dashboard
A dynamic command center that ditches generic pie charts for a proprietary **4-Pillar Wealth Index**. It continuously calculates a Money Health Score (0-100) based on:
* **FIRE Vector:** Savings & Investment ratios.
* **Discipline Vector:** Discretionary spending controls.
* **Leakage Index:** Tracking the "UPI Black Hole" (money wasted on sub-₹300 micro-transactions).
* **Credit Reliance:** Utilization of high-value credit.
* *Dynamic State:* Users can update their Monthly Income and Credit Limits in the sidebar, and the entire dashboard recalculates via session state memory in real-time.

### 2. The ET Wealth Bridge (Actionable Interventions)
Tracking expenses is not enough; the goal is to build wealth. The engine detects spending anomalies (e.g., Lifestyle Creep or High Food Spend) and recommends automated interventions. Users can instantly divert wasted capital into mock Auto-SIP mutual funds (e.g., Nifty India Consumption Index) with a single click.

### 3. RAG-Powered Financial Chatbot
A fully integrated, personalized AI mentor. The LLM is injected with the user's real-time financial metrics, Health Score, and a 20-transaction context window, allowing it to give strictly grounded, mathematically accurate financial advice without generic hallucinations.

### 4. Geospatial Merchant Directory
A centralized Ledger and Map that aggregates all resolved entities, allowing users to view their spending hotspots and verify the AI's confidence scores.

---

## 🏗️ System Architecture
The application utilizes a decoupled architecture to ensure scalability:
* **Backend:** `FastAPI` serves as the orchestration layer, handling SMS ingestion and agent routing.
* **Frontend:** `Streamlit` provides a reactive, state-driven user interface with custom CSS.
* **Database:** `SQLite` and `Pandas` handle the continuous mathematical aggregation of the transaction ledger.
* **AI Layer:** `Google GenAI SDK` (Gemini 2.5 Flash) drives both the backend Sherlock agent and the frontend RAG Chatbot.

---

## ⚙️ Local Setup & Installation

Follow these steps to run the application locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/spendsense-ai-backend.git](https://github.com/YourUsername/spendsense-ai-backend.git)
cd spendsense-ai-backend