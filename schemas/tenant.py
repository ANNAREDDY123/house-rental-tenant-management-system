from datetime import date

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class TenantCreate(BaseModel):

    name: str = Field(..., min_length=2, max_length=100)

    email: EmailStr

    phone: str = Field(..., min_length=10, max_length=10)

    aadhaar_number: str = Field(..., min_length=12, max_length=12)

    house_id: int

    move_in_date: date

    agreement_end_date: date


class TenantResponse(TenantCreate):

    id: int

    class Config:
        from_attributes = True
