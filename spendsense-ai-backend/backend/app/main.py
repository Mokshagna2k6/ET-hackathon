from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.models import EnrichedTransaction
from app.services.llm_parser import parse_sms
from app.services.enricher import enrich_transaction

app = FastAPI(
    title="SpendSense AI API",
    description="AMRE (Agentic Merchant Resolution Engine) Backend",
    version="1.0.0"
)

class SMSRequest(BaseModel):
    sms_text: str

@app.get("/")
def read_root():
    return {"status": "AMRE Server is online and listening! 🚀"}

@app.post("/api/v1/process-sms", response_model=EnrichedTransaction)
def process_transaction(request: SMSRequest):
    """
    Takes a raw bank SMS, extracts the data, researches the merchant, 
    and returns a fully enriched financial profile.
    """
    try:
        print(f"\n--- 📩 NEW SMS RECEIVED ---")
        print(f"Text: {request.sms_text}")
        
        print("Step 1: Parsing SMS with Gemini...")
        parsed_data = parse_sms(request.sms_text)
        
        print("Step 2: Enriching with Sherlock Agent (Web Search)...")
        enriched_data = enrich_transaction(parsed_data)
        
        print("--- ✅ PROCESSING COMPLETE ---")
        return enriched_data
        
    except Exception as e:
        print(f"🚨 API Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during AI processing")