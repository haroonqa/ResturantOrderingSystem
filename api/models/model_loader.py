from . import (
    orders,
    order_details,
    recipes,
    sandwiches,
    resources,
    menu_items,
    ingredients,
    ratings_reviews,
    customer
)
from .junction_tables import menu_item_ingredients  # Correct file for the junction table
from ..dependencies.database import engine  # Correct relative import

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
