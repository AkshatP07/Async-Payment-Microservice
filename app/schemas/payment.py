from pydantic import BaseModel


class PaymentCreate(BaseModel):
    amount: float

class PaymentOut(BaseModel):
    id: int

    amount: float
    status: str

    class Config:
        orm_mode = True
