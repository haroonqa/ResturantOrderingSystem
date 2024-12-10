from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=True)
    price = Column(DECIMAL(4, 2), nullable=False, server_default="0.0")
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    recipes = relationship(
        "Recipe",
        back_populates="sandwich",
        foreign_keys="Recipe.sandwich_id"
    )
    order_details = relationship("OrderDetail", back_populates="sandwich")
    menu_items = relationship("MenuItem", back_populates="sandwich")
