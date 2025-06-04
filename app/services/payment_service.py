from app.db.models import Payment
from app.db.session import SessionLocal

def create_payment(user_id: int, amount: float):
    db = SessionLocal()
    payment = Payment(user_id=user_id, amount=amount)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    db.close()
    return payment
