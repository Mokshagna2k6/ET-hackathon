from pydantic import BaseModel, Field
from typing import Optional

# 1. The Raw Extraction Model (From the SMS)
class TransactionData(BaseModel):
    merchant_name: str = Field(description="The clean name of the shop or business. E.g., 'Raju Tea Stall'")
    amount: float = Field(description="The exact amount of money spent")
    payment_method: str = Field(description="How it was paid (e.g., UPI, Card)")
    raw_upi_id: str = Field(description="The raw VPA/UPI ID if present, otherwise 'N/A'")

# 2. The Enriched Model (After Sherlock Agent investigates)
class EnrichedTransaction(BaseModel):
    transaction: TransactionData
    category: str = Field(description="e.g., Food & Dining, Shopping, Transport")
    confidence_score: float = Field(description="A score from 0.0 to 1.0 indicating AI confidence")
    is_suspicious: bool = Field(default=False, description="True if the merchant looks risky")