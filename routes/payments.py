from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.payment import Payment
from models.tenant import Tenant
from schemas.payment import PaymentCreate
from services.rental_service import valid_payment_status

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):

    tenant = db.query(Tenant).filter(
        Tenant.id == payment.tenant_id
    ).first()

    if not tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found."
        )

    duplicate = db.query(Payment).filter(
        Payment.tenant_id == payment.tenant_id,
        Payment.payment_month == payment.payment_month
    ).first()

    if duplicate:

        raise HTTPException(
            status_code=400,
            detail="Payment already exists for this month."
        )

    if not valid_payment_status(
        payment.payment_status
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid payment status."
        )

    db_payment = Payment(**payment.dict())

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment


@router.get("/")
def get_payments(
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Payment)

    if status:

        query = query.filter(
            Payment.payment_status == status
        )

    total = query.count()

    payments = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": payments
    }


@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found."
        )

    return payment


@router.put("/{payment_id}")
def update_payment(
    payment_id: int,
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):

    db_payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not db_payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found."
        )

    if not valid_payment_status(
        payment.payment_status
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid payment status."
        )

    duplicate = db.query(Payment).filter(
        Payment.tenant_id == payment.tenant_id,
        Payment.payment_month == payment.payment_month,
        Payment.id != payment_id
    ).first()

    if duplicate:

        raise HTTPException(
            status_code=400,
            detail="Duplicate monthly payment."
        )

    db_payment.tenant_id = payment.tenant_id
    db_payment.payment_month = payment.payment_month
    db_payment.amount = payment.amount
    db_payment.payment_date = payment.payment_date
    db_payment.payment_method = payment.payment_method
    db_payment.payment_status = payment.payment_status

    db.commit()
    db.refresh(db_payment)

    return db_payment


@router.delete("/{payment_id}")
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found."
        )

    db.delete(payment)
    db.commit()

    return {
        "message": "Payment deleted successfully."
    }


@router.get("/tenant/{tenant_id}/history")
def payment_history(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found."
        )

    return db.query(Payment).filter(
        Payment.tenant_id == tenant_id
    ).all()


@router.get("/reports/overdue")
def overdue_payments(
    db: Session = Depends(get_db)
):

    overdue = db.query(Payment).filter(
        Payment.payment_status == "Overdue"
    ).all()

    return {
        "total_overdue": len(overdue),
        "payments": overdue
    }
