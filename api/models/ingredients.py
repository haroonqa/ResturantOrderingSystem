from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from ..dependencies.database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String(100), nullable=False)

    menu_items = relationship("MenuItem", secondary="menu_item_ingredients", back_populates="ingredients")

    @validates("quantity")
    def validate_quantity(self, key, value):
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        return value
