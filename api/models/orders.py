from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"
    
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_completed = Column(Boolean, default=False)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"))
    takeout = Column(Boolean, default=True)
    delivery = Column(Boolean, default=False)
    order_details = relationship("OrderDetail", back_populates="order")
    transaction = relationship("Transaction", back_populates="order")
    promotion_id = Column(Integer, ForeignKey("promotion.id"), nullable=True)
    promotion = relationship("Promotion", back_populates="orders", lazy="selectin")