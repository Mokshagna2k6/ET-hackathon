import random
from sqlalchemy.orm import Session
from app.database import SessionLocal, TransactionDB, init_db

def seed_database():
    """Injects highly realistic, production-grade mock data into the database."""
    print("🌱 Starting database seeding process...")
    
    init_db()
    db: Session = SessionLocal()
    
    db.query(TransactionDB).delete()
    db.commit()
    
    transactions_to_insert = []

    food_merchants = [
        ("Zomato", "zomato@hdfcbank", "Food & Dining"),
        ("Swiggy", "swiggy@icici", "Food & Dining"),
        ("Zepto", "zepto@yesbank", "Groceries"),
        ("Blinkit", "blinkit@paytm", "Groceries"),
        ("Local Chai Tapri", "tea.stall@sbi", "Food & Dining")
    ]
    for _ in range(45):
        merchant, upi, cat = random.choice(food_merchants)
        transactions_to_insert.append(
            TransactionDB(
                merchant_name=merchant,
                amount=round(random.uniform(60, 290), 2),
                payment_method="UPI",
                raw_upi_id=upi,
                category=cat,
                confidence_score=1.0,
                is_suspicious=False
            )
        )

    ecom_merchants = [
        ("Meesho", "fashnear@yesbank", "Shopping / E-commerce"),
        ("Amazon India", "amazon@icici", "Shopping / E-commerce"),
        ("Myntra", "myntra@kotak", "Shopping / E-commerce")
    ]
    for _ in range(8):
        merchant, upi, cat = random.choice(ecom_merchants)
        transactions_to_insert.append(
            TransactionDB(
                merchant_name=merchant,
                amount=round(random.uniform(1500, 4500), 2),
                payment_method="UPI",
                raw_upi_id=upi,
                category=cat,
                confidence_score=0.98,
                is_suspicious=False
            )
        )

    routine_expenses = [
        ("Jio Prepaid", "jio@sbi", "Utilities", 749.0),
        ("Spotify Premium", "spotify@hdfc", "Entertainment", 119.0),
        ("IIT Patna Fee Desk", "iitp.fees@sbi", "Education", 4500.0),
        ("Codeforces Premium", "codeforces@stripe", "Software/SaaS", 850.0),
        ("Delta Exchange", "delta.crypto@axis", "Financial Services", 10000.0)
    ]
    for merchant, upi, cat, amount in routine_expenses:
        transactions_to_insert.append(
            TransactionDB(
                merchant_name=merchant,
                amount=amount,
                payment_method="UPI/Card",
                raw_upi_id=upi,
                category=cat,
                confidence_score=0.99,
                is_suspicious=False
            )
        )

    db.add_all(transactions_to_insert)
    db.commit()
    db.close()
    
    print(f"✅ Successfully injected {len(transactions_to_insert)} real-world transactions into 'transactions.db'!")

if __name__ == "__main__":
    seed_database()