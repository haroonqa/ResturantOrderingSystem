from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.sandwiches import Sandwich
from ..schemas.sandwiches import SandwichCreate, SandwichUpdate

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def create_sandwich(db, sandwich_data):
    try:
        new_sandwich = Sandwich(**sandwich_data.dict())
        db.add(new_sandwich)
        db.commit()
        db.refresh(new_sandwich)
        return new_sandwich
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction to avoid corrupt state
        # Check for specific foreign key constraint error
        if "a foreign key constraint fails" in str(e):
            raise HTTPException(
                status_code=400,
                detail="The provided recipe_id does not exist. Please create the recipe first."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while creating the sandwich."
            )

def get_all_sandwiches(db: Session):
    return db.query(Sandwich).all()

def get_sandwich_by_id(db: Session, sandwich_id: int):
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    return sandwich

def update_sandwich(db: Session, sandwich_id: int, request: SandwichUpdate):
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    
    # Update only the provided fields
    for key, value in request.dict(exclude_unset=True).items():
        setattr(sandwich, key, value)
    db.commit()
    db.refresh(sandwich)
    return sandwich

def delete_sandwich(db: Session, sandwich_id: int):
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    db.delete(sandwich)
    db.commit()
