import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models import TransactionData

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0 
)

structured_llm = llm.with_structured_output(TransactionData)

def parse_sms(sms_text: str) -> TransactionData:
    """
    Takes a raw SMS string, passes it to Gemini, and returns structured JSON.
    """
    try:
        result = structured_llm.invoke(sms_text)
        return result
    except Exception as e:
        print(f"Error parsing SMS: {e}")
        return TransactionData(
            merchant_name="Unknown", 
            amount=0.0, 
            payment_method="Unknown", 
            raw_upi_id="N/A"
        )