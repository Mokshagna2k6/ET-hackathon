import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models import TransactionData

# Load environment variables (API Keys)
load_dotenv()

# Initialize the blazing fast Gemini 2.5 Flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0 
)

# Bind our strict Pydantic rules to the LLM
structured_llm = llm.with_structured_output(TransactionData)

def parse_sms(sms_text: str) -> TransactionData:
    """
    Takes a raw SMS string, passes it to Gemini, and returns structured JSON.
    """
    try:
        # Ask the AI to extract the data
        result = structured_llm.invoke(sms_text)
        return result
    except Exception as e:
        print(f"Error parsing SMS: {e}")
        # Return a safe fallback if the AI fails completely
        return TransactionData(
            merchant_name="Unknown", 
            amount=0.0, 
            payment_method="Unknown", 
            raw_upi_id="N/A"
        )