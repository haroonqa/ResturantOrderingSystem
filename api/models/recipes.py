from sqlalchemy import Column, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id", ondelete="CASCADE"), nullable=True)
    ingredients_needed = Column(JSON, default=[
        {"ingredient_id": 1, "amount": 1},
        {"ingredient_id": 2, "amount": 2}
    ])

    # Relationships
    sandwich = relationship(
        "Sandwich",
        back_populates="recipes",
        foreign_keys=[sandwich_id]  # Explicitly specify the foreign key
    )
