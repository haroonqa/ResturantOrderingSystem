from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..dependencies.database import get_db
from ..schemas.menu_items import MenuItem, MenuItemFilter
from ..services.menu_search import search_menu_items, get_categories, get_dietary_types

router = APIRouter(
    prefix="/menu",
    tags=["Menu Search"]
)


@router.get("/search", response_model=List[MenuItem])
def search_menu(
    search_term: Optional[str] = None,
    category: Optional[str] = None,
    dietary_type: Optional[str] = None,
    max_price: Optional[float] = None,
    max_calories: Optional[int] = None,
    tags: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Search menu items with various filters:
    - Text search in name, description, and tags
    - Category filter (e.g., appetizers, main course)
    - Dietary type filter (e.g., vegetarian, vegan)
    - Maximum price
    - Maximum calories
    - Tags
    """
    return search_menu_items(
        db,
        search_term=search_term,
        category=category,
        dietary_type=dietary_type,
        max_price=max_price,
        max_calories=max_calories,
        tags=tags
    )


@router.get("/categories", response_model=List[str])
def list_categories(db: Session = Depends(get_db)):
    """Get all available menu categories"""
    return get_categories(db)


@router.get("/dietary-types", response_model=List[str])
def list_dietary_types(db: Session = Depends(get_db)):
    """Get all available dietary types"""
    return get_dietary_types(db)
