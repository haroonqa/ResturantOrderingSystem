from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    calories = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)
    
    reviews = relationship("RatingsReviews", back_populates="menu_item")
    ingredients = relationship("Ingredient", secondary="menu_item_ingredients", back_populates="menu_items")
