from ..dependencies.database import Base, engine
from . import (
    customer,
    menu_items,
    ingredients,
    orders,
    order_details,
    ratings_reviews,
    staff,
    transactions,
    recipes,
    sandwiches,
    resources,
    promotion,
    menu_item_ingredients

    
)
from .junction_tables import menu_item_ingredients  # Correct file for the junction table
from ..dependencies.database import engine

def index():
    # Create tables for all models
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    ingredients.Base.metadata.create_all(engine)
    ratings_reviews.Base.metadata.create_all(engine)
    customer.Base.metadata.create_all(engine)
    menu_item_ingredients.create(engine, checkfirst=True)
    transactions.Base.metadata.create_all(engine)
    staff.Base.metadata.create_all(engine)
    promotion.Base.metadata.create_all(engine)
