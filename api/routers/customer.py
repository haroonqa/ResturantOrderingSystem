from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import customer as controller
from ..schemas import customer as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Customer'],
    prefix="/customer"
)

# these endpoints are for current customers or people who want to create an account 
@router.post("/", response_model=schema.Customer)
def create(request: schema.CustomerCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Customer])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{customer_id}", response_model=schema.Customer)
def read_one(customer_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, customer_id=customer_id)

# these endpoints are for guests
@router.post("/guest", response_model=schema.GuestCreate)
def create_guest(email: str, phone_number: str, db: Session = Depends(get_db)):
    request = schema.CustomerCreate(email=email, phone_number=phone_number)
    return controller.create_guest(db=db, request=request)


@router.get("/guest/{guest_id}", response_model=schema.GuestResponse)
def read_guest(guest_id: int, db: Session = Depends(get_db)):
    return controller.read_guest(db, guest_id=guest_id)


@router.delete("/guest/{guest_id}")
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    return controller.delete_guest(db, guest_id=guest_id)
