from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class House(Base):

    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)

    house_name = Column(String(100), nullable=False)

    address = Column(String(255), nullable=False)

    rent_amount = Column(Float, nullable=False)

    house_type = Column(String(50), nullable=False)

    availability_status = Column(String(30), nullable=False)
