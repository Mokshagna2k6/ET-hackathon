# 💸 SpendSense AI: Agentic Merchant Resolution Engine (AMRE)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg)
![Gemini](https://img.shields.io/badge/AI-Gemini_2.5_Flash-orange.svg)

**SpendSense AI** transforms messy, unstructured bank SMS messages into clean, enriched, and categorized financial data using a multi-agent AI pipeline. 

---

## 🚀 The Problem
Bank SMS notifications are notoriously cryptic. A transaction might read `"Rs 450 to VPA-fashnear@yesbank"`, leaving users confused and financial apps with poor analytics. Traditional regex parsers fail because they cannot *reason* about the text or resolve obscure holding-company names.

## 💡 The Solution: AMRE
The **Agentic Merchant Resolution Engine (AMRE)** solves this using a two-step AI architecture:
1. **The Extractor:** An LLM instantly isolates the raw facts (Amount, Date, raw UPI ID).
2. **The Sherlock Agent:** An autonomous web-research agent that takes cryptic IDs (like `fashnear`), searches the internet, and resolves them to their real-world brand names (e.g., `Meesho`), assigning a business category and a confidence/security score.

## ✨ Key Features
* **🧠 Agentic Enrichment:** Uses LangChain and Tavily to dynamically research unknown merchants on the web.
* **⚡ Smart Database Caching:** Uses SQLAlchemy to fingerprint merchants by their static UPI ID. Once a merchant is researched, it is cached in the SQL database. Future transactions from that merchant are resolved in milliseconds without needing an API call ("Fast Hits").
* **📊 Real-Time Analytics:** A Streamlit dashboard providing macro-level insights, category breakdowns, and a unified ledger of all processed transactions.
* **🗺️ Geospatial Mapping:** Visualizes the geographic distribution of resolved merchant terminals.
* **🛡️ Bulletproof Pydantic Guards:** Ensures the AI strictly outputs formatted JSON, preventing app crashes.

---

## 🏗️ Architecture & Tech Stack

* **Frontend:** Streamlit (Python)
* **Backend:** FastAPI (Python)
* **Database:** SQLite (via SQLAlchemy) - *Easily scalable to PostgreSQL*
* **AI Parser & Formatter:** Google Gemini 2.5 Flash
* **Agentic Web Search:** LangChain + Tavily API

---

## 🛠️ Installation & Setup

**1. Clone the repository and navigate to the project root:**
```bash
git clone [https://github.com/yourusername/SpendSense-AI.git](https://github.com/yourusername/SpendSense-AI.git)
cd SpendSense-AI