from ..dependencies.database import Base, engine
from . import (
    customer,
    menu_items,
    ingredients,
    orders,
    order_details,
    ratings_reviews,
    promotion,
)

def index():
    # Create all tables at once
    Base.metadata.create_all(engine)
