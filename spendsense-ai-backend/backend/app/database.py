import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from app.models import EnrichedTransaction

SQLALCHEMY_DATABASE_URL = "sqlite:///../data/transactions.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TransactionDB(Base):
    """This defines exactly how the data looks inside the SQL database."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    merchant_name = Column(String, index=True)
    amount = Column(Float)
    payment_method = Column(String)
    raw_upi_id = Column(String, index=True)
    category = Column(String)
    confidence_score = Column(Float)
    is_suspicious = Column(Boolean)


def init_db():
    """Generates the SQL tables based on the schema above."""
    os.makedirs(os.path.dirname("../data/transactions.db"), exist_ok=True)
    Base.metadata.create_all(bind=engine)
    print("🗄️ SQL Tables Initialized.")

def save_transaction(enriched_data: EnrichedTransaction):
    """Opens a secure SQL session, inserts data, and closes the connection."""
    db = SessionLocal()
    try:
   
        db_transaction = TransactionDB(
            merchant_name=enriched_data.transaction.merchant_name,
            amount=enriched_data.transaction.amount,
            payment_method=enriched_data.transaction.payment_method,
            raw_upi_id=enriched_data.transaction.raw_upi_id,
            category=enriched_data.category,
            confidence_score=enriched_data.confidence_score,
            is_suspicious=enriched_data.is_suspicious
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        print(f"💾 Saved to SQL DB: {db_transaction.merchant_name}")
    finally:
        db.close()

def get_merchant_by_upi_id(upi_id: str):
    """
    THE CACHING LAYER: Checks the database to see if we already know 
    this merchant's details before waking up the AI agent.
    """
    if not upi_id or upi_id == "N/A":
        return None
        
    db = SessionLocal()
    try:
        
        result = db.query(TransactionDB).filter(TransactionDB.raw_upi_id == upi_id).first()
        
        if result:
           
            return {
                "resolved_merchant_name": result.merchant_name,
                "category": result.category,
                "confidence_score": 1.0, 
                "is_suspicious": result.is_suspicious
            }
        return None
    finally:
        db.close()