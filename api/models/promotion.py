from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    discount_percentage = Column(Integer, nullable=False)
    expiration_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    orders = relationship("Order", back_populates="promotion", lazy="selectin", cascade="all, delete-orphan")
