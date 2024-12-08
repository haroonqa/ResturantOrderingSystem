from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import staff as controller
from ..schemas import staff as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Staff'],
    prefix="/staff"
)

@router.post("/", response_model=schema.StaffCreate)
def create_staff(staff: schema.StaffCreate, db: Session = Depends(get_db)):
    return controller.create_staff(db=db, staff=staff)

@router.get("/", response_model=list[schema.StaffBase])
def read_all_staff(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{staff_id}", response_model=schema.StaffBase)
def read_staff(staff_id: int, db: Session = Depends(get_db)):
    return controller.read_staff(db=db, staff_id=staff_id)

@router.put("/{staff_id}", response_model=schema.StaffBase)
def update_staff(staff_id: int, staff: schema.StaffUpdate, db: Session = Depends(get_db)):
    return controller.update_staff(db=db, staff_id=staff_id, staff_update=staff)

@router.delete("/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    controller.delete_staff(db=db, staff_id=staff_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

