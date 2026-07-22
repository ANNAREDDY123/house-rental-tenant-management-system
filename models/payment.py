from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from database import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        nullable=False
    )

    payment_month = Column(String(20), nullable=False)

    amount = Column(Float, nullable=False)

    payment_date = Column(Date, nullable=False)

    payment_method = Column(String(50), nullable=False)

    payment_status = Column(String(20), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "payment_month",
            name="unique_monthly_payment"
        ),
    )
