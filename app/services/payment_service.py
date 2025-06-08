from app.db.models import Payment
from app.db.session import AsyncSessionLocal

def create_payment(user_id: int, amount: float):
    db = AsyncSessionLocal()
    payment = Payment(user_id=user_id, amount=amount)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    db.close()
    return payment
