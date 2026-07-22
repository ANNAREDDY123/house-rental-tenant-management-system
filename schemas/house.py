from pydantic import BaseModel
from pydantic import Field


class HouseCreate(BaseModel):

    house_name: str = Field(..., min_length=2, max_length=100)

    address: str = Field(..., min_length=5)

    rent_amount: float = Field(..., gt=0)

    house_type: str

    availability_status: str


class HouseResponse(HouseCreate):

    id: int

    class Config:
        from_attributes = True
