from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from ..models import staff as model
from ..schemas import staff as schema


def create_staff(db: Session, staff: schema.StaffCreate): 
    try:
        db_staff = model.Staff(username=staff.username) 
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)
        return db_staff
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_all(db: Session):
    try:
        result = db.query(model.Staff).all()  # Ensure correct model reference
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result