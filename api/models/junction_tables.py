from sqlalchemy import Table, Column, Integer, ForeignKey
from ..dependencies.database import Base

menu_item_ingredients = Table(
    "menu_item_ingredients",
    Base.metadata,
    Column("menu_item_id", Integer, ForeignKey("menu_items.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True)
)

