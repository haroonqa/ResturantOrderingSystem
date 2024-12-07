from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.menu_items import MenuItem


def search_menu_items(
    db: Session,
    search_term: str = None,
    category: str = None,
    dietary_type: str = None,
    max_price: float = None,
    max_calories: int = None,
    tags: list = None
):
    query = db.query(MenuItem)
    
    # Apply text search filter
    if search_term:
        query = query.filter(
            or_(
                MenuItem.name.ilike(f"%{search_term}%"),
                MenuItem.description.ilike(f"%{search_term}%"),
                MenuItem.tags.ilike(f"%{search_term}%")
            )
        )
    
    # Apply category filter
    if category:
        query = query.filter(MenuItem.category == category)
    
    # Apply dietary type filter (vegetarian, vegan, etc.)
    if dietary_type:
        query = query.filter(MenuItem.dietary_type == dietary_type)
    
    # Apply price range filter
    if max_price:
        query = query.filter(MenuItem.price <= max_price)
    
    # Apply calorie range filter
    if max_calories:
        query = query.filter(MenuItem.calories <= max_calories)
    
    # Apply tag filters
    if tags:
        for tag in tags:
            query = query.filter(MenuItem.tags.ilike(f"%{tag}%"))
    
    return query.all()


def get_categories(db: Session):
    """Get all unique categories"""
    return [cat[0] for cat in db.query(MenuItem.category).distinct().all() if cat[0]]


def get_dietary_types(db: Session):
    """Get all unique dietary types"""
    return [dt[0] for dt in db.query(MenuItem.dietary_type).distinct().all() if dt[0]]
