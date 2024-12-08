from sqlalchemy.orm import Session
from ..models.ingredients import Ingredient
from ..models.menu_items import MenuItem
from fastapi import HTTPException, status
from typing import List, Dict
from sqlalchemy import and_

class InsufficientIngredientsError(Exception):
    pass

def check_and_update_ingredients(db: Session, menu_item_id: int, quantity: int = 1) -> bool:
    """
    Check if there are sufficient ingredients for a menu item and update quantities if there are.
    Returns True if successful, raises InsufficientIngredientsError if ingredients are insufficient.
    """
    # Get the menu item and its required ingredients
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Check if we have enough of each ingredient
    insufficient_ingredients = []
    required_quantities = {}
    
    for ingredient in menu_item.ingredients:
        # Calculate required quantity (assuming 1 unit per menu item, adjust as needed)
        required_qty = quantity  # Multiply by recipe quantity if you have that relationship
        required_quantities[ingredient.id] = required_qty
        
        if ingredient.quantity < required_qty:
            insufficient_ingredients.append(ingredient.name)
    
    if insufficient_ingredients:
        raise InsufficientIngredientsError(
            f"Insufficient quantities of: {', '.join(insufficient_ingredients)}"
        )
    
    # If we have enough, update the quantities
    for ingredient in menu_item.ingredients:
        ingredient.quantity -= required_quantities[ingredient.id]
        # Check if we need to set low stock alert
        ingredient.low_stock_alert = ingredient.quantity <= ingredient.min_threshold
    
    db.commit()
    return True

def get_low_stock_ingredients(db: Session) -> List[Dict]:
    """
    Get all ingredients that are below their minimum threshold.
    """
    low_stock = db.query(Ingredient).filter(
        and_(
            Ingredient.quantity <= Ingredient.min_threshold,
            Ingredient.low_stock_alert == True
        )
    ).all()
    
    return [
        {
            "id": ingredient.id,
            "name": ingredient.name,
            "current_quantity": ingredient.quantity,
            "min_threshold": ingredient.min_threshold,
            "unit": ingredient.unit
        }
        for ingredient in low_stock
    ]

def restock_ingredient(db: Session, ingredient_id: int, quantity: int) -> Dict:
    """
    Restock an ingredient with the specified quantity.
    """
    if quantity <= 0:
        raise ValueError("Restock quantity must be positive")

    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    ingredient.quantity += quantity
    ingredient.low_stock_alert = ingredient.quantity <= ingredient.min_threshold
    db.commit()
    
    return {
        "id": ingredient.id,
        "name": ingredient.name,
        "new_quantity": ingredient.quantity,
        "unit": ingredient.unit,
        "low_stock_alert": ingredient.low_stock_alert
    }
