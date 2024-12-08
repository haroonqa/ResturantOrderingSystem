from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    default_resource_list = [
        {
            "resource_id": 1,
            "amount" : 1
        },
        {
            "resource_id": 2,
            "amount": 2
        }
    
    ]

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    resources_needed = Column(JSON, default=default_resource_list)

    sandwich = relationship("Sandwich", back_populates="recipes")
    #resource = relationship("Resource", back_populates="recipes")