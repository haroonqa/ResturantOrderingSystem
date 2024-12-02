from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    resources_needed = Column(JSON)

    sandwich = relationship("Sandwich", back_populates="recipes")
    resource = relationship("Resource", back_populates="recipes")