from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.house import House
from schemas.house import HouseCreate
from services.rental_service import valid_house_status

router = APIRouter(
    prefix="/houses",
    tags=["Houses"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_house(
    house: HouseCreate,
    db: Session = Depends(get_db)
):

    if not valid_house_status(house.availability_status):

        raise HTTPException(
            status_code=400,
            detail="Invalid house status."
        )

    db_house = House(**house.dict())

    db.add(db_house)
    db.commit()
    db.refresh(db_house)

    return db_house


@router.get("/")
def get_houses(
    address: str = None,
    house_type: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(House)

    if address:
        query = query.filter(House.address.contains(address))

    if house_type:
        query = query.filter(House.house_type.contains(house_type))

    if status:
        query = query.filter(House.availability_status == status)

    total = query.count()

    houses = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": houses
    }


@router.get("/{house_id}")
def get_house(
    house_id: int,
    db: Session = Depends(get_db)
):

    house = db.query(House).filter(
        House.id == house_id
    ).first()

    if not house:

        raise HTTPException(
            status_code=404,
            detail="House not found."
        )

    return house


@router.put("/{house_id}")
def update_house(
    house_id: int,
    house: HouseCreate,
    db: Session = Depends(get_db)
):

    db_house = db.query(House).filter(
        House.id == house_id
    ).first()

    if not db_house:

        raise HTTPException(
            status_code=404,
            detail="House not found."
        )

    db_house.house_name = house.house_name
    db_house.address = house.address
    db_house.rent_amount = house.rent_amount
    db_house.house_type = house.house_type
    db_house.availability_status = house.availability_status

    db.commit()
    db.refresh(db_house)

    return db_house


@router.delete("/{house_id}")
def delete_house(
    house_id: int,
    db: Session = Depends(get_db)
):

    house = db.query(House).filter(
        House.id == house_id
    ).first()

    if not house:

        raise HTTPException(
            status_code=404,
            detail="House not found."
        )

    db.delete(house)
    db.commit()

    return {
        "message": "House deleted successfully."
    }
