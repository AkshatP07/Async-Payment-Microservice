from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PaymentStatusEnum(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Float)
    status = Column(String, default="pending")
