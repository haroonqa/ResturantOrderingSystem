from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from .promotion import Promotion


class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    promotion_id: Optional[int] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    promotion_id: Optional[int] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None
    promotion: Optional[Promotion] = None

    class Config:
        from_attributes = True
