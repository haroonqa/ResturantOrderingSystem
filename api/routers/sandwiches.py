from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.sandwiches import SandwichCreate, SandwichUpdate, Sandwich
from ..dependencies.database import get_db
from ..controllers.sandwiches import (
    create_sandwich,
    get_all_sandwiches,
    get_sandwich_by_id,
    update_sandwich,
    delete_sandwich,
)

router = APIRouter(
    prefix="/sandwiches",
    tags=["Sandwiches"]
)

@router.post("/", response_model=Sandwich, status_code=status.HTTP_201_CREATED)
def create(request: SandwichCreate, db: Session = Depends(get_db)):
    return create_sandwich(db, request)

@router.get("/", response_model=list[Sandwich])
def read_all(db: Session = Depends(get_db)):
    return get_all_sandwiches(db)

@router.get("/{sandwich_id}", response_model=Sandwich)
def read_one(sandwich_id: int, db: Session = Depends(get_db)):
    return get_sandwich_by_id(db, sandwich_id)

@router.put("/{sandwich_id}", response_model=Sandwich)
def update(sandwich_id: int, request: SandwichUpdate, db: Session = Depends(get_db)):
    return update_sandwich(db, sandwich_id, request)

@router.delete("/{sandwich_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(sandwich_id: int, db: Session = Depends(get_db)):
    delete_sandwich(db, sandwich_id)
    return {"detail": "Sandwich deleted successfully"}
