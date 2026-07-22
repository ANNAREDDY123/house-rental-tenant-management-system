from datetime import date

from pydantic import BaseModel
from pydantic import Field


class PaymentCreate(BaseModel):

    tenant_id: int

    payment_month: str

    amount: float = Field(..., gt=0)

    payment_date: date

    payment_method: str

    payment_status: str


class PaymentResponse(PaymentCreate):

    id: int

    class Config:
        from_attributes = True
