from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from database import Base


class Tenant(Base):

    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    phone = Column(String(15), nullable=False)

    aadhaar_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    house_id = Column(
        Integer,
        ForeignKey("houses.id"),
        nullable=False
    )

    move_in_date = Column(Date, nullable=False)

    agreement_end_date = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "house_id",
            name="unique_house_tenant"
        ),
    )
