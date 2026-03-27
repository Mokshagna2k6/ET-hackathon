import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
from pydantic import BaseModel, Field

# Import the models you created in step 1
from app.models import TransactionData, EnrichedTransaction

load_dotenv()

# --- 1. SET UP THE AGENT (THE RESEARCHER) ---
search_tool = TavilySearchResults(max_results=3)
tools = [search_tool]
agent_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

system_prompt = """You are AMRE (Agentic Merchant Resolution Engine). 
Investigate the merchant name or UPI ID using the search tool. 
Find the real company name, business category, and check if it is a known scam/suspicious."""

agent_executor = create_agent(agent_llm, tools, system_prompt=system_prompt)

# --- 2. SET UP THE FORMATTER (THE STRICT BOUNCER) ---
# We need a temporary model just for the enrichment fields
class EnrichmentData(BaseModel):
    category: str = Field(description="e.g., Food & Dining, Shopping, Financial Services, Transport")
    confidence_score: float = Field(description="Confidence from 0.0 to 1.0")
    is_suspicious: bool = Field(description="True if risky or scam")
    resolved_merchant_name: str = Field(description="The clean, real-world brand name")

formatter_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
structured_formatter = formatter_llm.with_structured_output(EnrichmentData)

# --- 3. THE MAIN FUNCTION ---
def enrich_transaction(parsed_tx: TransactionData) -> EnrichedTransaction:
    """
    Takes the basic parsed SMS, researches the merchant, and returns the full enriched profile.
    """
    # Decide what to search: The raw UPI ID is usually better than the messy name
    query = parsed_tx.raw_upi_id if parsed_tx.raw_upi_id != "N/A" else parsed_tx.merchant_name
    
    try:
        print(f"\n🕵️‍♂️ AMRE researching: {query}...")
        
        # Step A: Agent does the web research
        agent_response = agent_executor.invoke({"messages": [("user", f"Investigate this merchant/UPI: {query}")]})
        
        # Safely extract the text response
        raw_content = agent_response["messages"][-1].content
        research_notes = raw_content[0]['text'] if isinstance(raw_content, list) else raw_content
        
        print(f"🧠 Formatting research into strict JSON...")
        
        # Step B: Formatter converts messy notes into strict Pydantic JSON
        format_prompt = f"Based on these research notes: {research_notes}\nExtract the category, confidence, suspicion, and real merchant name."
        structured_data = structured_formatter.invoke(format_prompt)
        
        # Override the original raw name with the newly discovered clean name!
        parsed_tx.merchant_name = structured_data.resolved_merchant_name
        
        # Combine into the final EnrichedTransaction
        return EnrichedTransaction(
            transaction=parsed_tx,
            category=structured_data.category,
            confidence_score=structured_data.confidence_score,
            is_suspicious=structured_data.is_suspicious
        )
        
    except Exception as e:
        print(f"Error enriching transaction: {e}")
        # Bulletproof Fallback: If internet goes down, return a safe default
        return EnrichedTransaction(
            transaction=parsed_tx,
            category="Unknown",
            confidence_score=0.0,
            is_suspicious=False
        )