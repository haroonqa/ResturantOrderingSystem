from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    price = Column(DECIMAL(4, 2), nullable=False, server_default='0.0')
    payment_method = Column(String(4), nullable=False)

    order = relationship("Order", back_populates="transaction")