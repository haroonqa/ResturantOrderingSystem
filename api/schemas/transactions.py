from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime
from .orders import Order  # Assuming Order schema is defined elsewhere

# Base schema for common fields
class TransactionBase(BaseModel):
    price: float
    payment_method: str

# Schema for creating a new transaction
class TransactionCreate(TransactionBase):
    order_id: int

# Schema for updating an existing transaction
class TransactionUpdate(BaseModel):
    order_id: Optional[int] = None
    price: Optional[float] = None
    payment_method: Optional[str] = None

# Schema for reading a transaction (output schema)
class Transaction(TransactionBase):
    id: int
    order: Optional[Order] = None  # Include the related Order, if applicable

    class Config:
        orm_mode = True  # Use orm_mode for SQLAlchemy integration
