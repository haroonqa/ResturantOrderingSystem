from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.ingredients import Ingredient
from ..schemas.ingredients import IngredientCreate, IngredientResponse, IngredientUpdate


def create_ingredient(db: Session, request: IngredientCreate) -> IngredientResponse:
    new_ingredient = Ingredient(**request.dict())
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient


def get_all_ingredients(db: Session):
    return db.query(Ingredient).all()


def get_ingredient(db: Session, ingredient_id: int):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Ingredient not found"
)
    return ingredient


def delete_ingredient(db: Session, ingredient_id: int):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Ingredient not found"
)
    db.delete(ingredient)
    db.commit()


def update_ingredient(db: Session, ingredient_id: int, request: IngredientUpdate):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Ingredient not found"
)
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ingredient, key, value)
    db.commit()
    db.refresh(ingredient)
    return ingredient
