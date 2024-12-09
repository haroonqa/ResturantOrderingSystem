from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
from .sandwiches import Sandwich

class MenuItem(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    calories = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)
    dietary_type = Column(String(50), nullable=True)  # vegetarian, vegan, etc.
    description = Column(String(500), nullable=True)  # Detailed description
    tags = Column(String(200), nullable=True)  # Comma-separated tags
    
    reviews = relationship("RatingsReviews", back_populates="menu_item")
    ingredients = relationship("Ingredient", secondary="menu_item_ingredients", back_populates="menu_items")
    sandwich_id = Column(Integer, ForeignKey('sandwiches.id'), nullable=True)
    sandwich = relationship("Sandwich", back_populates="menu_items")
