from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..services.ingredient_tracking import get_low_stock_ingredients, restock_ingredient
from typing import List, Dict

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory Management"]
)

@router.get("/low-stock", response_model=List[Dict])
def check_low_stock(db: Session = Depends(get_db)):
    """
    Get a list of all ingredients that are below their minimum threshold.
    """
    return get_low_stock_ingredients(db)

@router.post("/restock/{ingredient_id}")
def restock(ingredient_id: int, quantity: int, db: Session = Depends(get_db)):
    """
    Restock a specific ingredient with the given quantity.
    """
    return restock_ingredient(db, ingredient_id, quantity)
