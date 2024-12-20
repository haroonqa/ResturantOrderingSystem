from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from .promotion import Promotion


class OrderBase(BaseModel):
    customer_id: int
    order_completed: Optional[bool] = False
    promotion_id: Optional[int] = None
    takeout: Optional[bool] = False
    delivery: Optional[bool] = False


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    customer_id: Optional[int]


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    

    class Config:
        from_attributes = True
