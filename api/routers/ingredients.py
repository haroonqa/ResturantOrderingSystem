from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.ingredients import IngredientCreate, IngredientResponse, IngredientUpdate
from ..controllers.ingredients import (
    create_ingredient,
    get_all_ingredients,
    get_ingredient,
    delete_ingredient,
    update_ingredient,
)

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)


@router.post("/", response_model=IngredientResponse)
def create(request: IngredientCreate, db: Session = Depends(get_db)):
    return create_ingredient(db, request)


@router.get("/", response_model=list[IngredientResponse])
def read_all(db: Session = Depends(get_db)):
    return get_all_ingredients(db)


@router.get("/{ingredient_id}", response_model=IngredientResponse)
def read_one(ingredient_id: int, db: Session = Depends(get_db)):
    return get_ingredient(db, ingredient_id)


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(ingredient_id: int, db: Session = Depends(get_db)):
    delete_ingredient(db, ingredient_id)
    return {"detail": "Ingredient deleted successfully"}


@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update(ingredient_id: int, request: IngredientUpdate, db: Session = Depends(get_db)):
    return update_ingredient(db, ingredient_id, request)
