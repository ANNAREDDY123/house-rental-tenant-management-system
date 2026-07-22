from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.house import House
from models.tenant import Tenant
from schemas.tenant import TenantCreate
from services.rental_service import (
    valid_agreement_dates,
    house_available
)

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_tenant(
    tenant: TenantCreate,
    db: Session = Depends(get_db)
):

    existing_email = db.query(Tenant).filter(
        Tenant.email == tenant.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    existing_aadhaar = db.query(Tenant).filter(
        Tenant.aadhaar_number == tenant.aadhaar_number
    ).first()

    if existing_aadhaar:

        raise HTTPException(
            status_code=400,
            detail="Aadhaar number already exists."
        )

    house = db.query(House).filter(
        House.id == tenant.house_id
    ).first()

    if not house:

        raise HTTPException(
            status_code=404,
            detail="House not found."
        )

    if not house_available(
        house.availability_status
    ):

        raise HTTPException(
            status_code=400,
            detail="House is not available."
        )

    if not valid_agreement_dates(
        tenant.move_in_date,
        tenant.agreement_end_date
    ):

        raise HTTPException(
            status_code=400,
            detail="Agreement end date must be after move-in date."
        )

    db_tenant = Tenant(**tenant.dict())

    db.add(db_tenant)

    house.availability_status = "Occupied"

    db.commit()
    db.refresh(db_tenant)

    return db_tenant


@router.get("/")
def get_tenants(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    total = db.query(Tenant).count()

    tenants = db.query(Tenant).offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": tenants
    }


@router.get("/{tenant_id}")
def get_tenant(
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

    return tenant


@router.put("/{tenant_id}")
def update_tenant(
    tenant_id: int,
    tenant: TenantCreate,
    db: Session = Depends(get_db)
):

    db_tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not db_tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found."
        )

    db_tenant.name = tenant.name
    db_tenant.email = tenant.email
    db_tenant.phone = tenant.phone
    db_tenant.aadhaar_number = tenant.aadhaar_number
    db_tenant.house_id = tenant.house_id
    db_tenant.move_in_date = tenant.move_in_date
    db_tenant.agreement_end_date = tenant.agreement_end_date

    db.commit()
    db.refresh(db_tenant)

    return db_tenant


@router.delete("/{tenant_id}")
def delete_tenant(
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

    house = db.query(House).filter(
        House.id == tenant.house_id
    ).first()

    if house:

        house.availability_status = "Available"

    db.delete(tenant)
    db.commit()

    return {
        "message": "Tenant deleted successfully."
    }
