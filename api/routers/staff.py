from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import staff as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Staff'],
    prefix="/staff"
)

@router.post("/", response_model=schema.StaffCreate)
def create_staff(staff: schema.StaffCreate, db: Session = Depends(get_db)):
    return controller.create_staff(db=db, staff=staff)

# @router.get("/", response_model=list[schema.Staff])
# def read_all_staff(db: Session = Depends(get_db)):
#     return controller.read_all(db)

