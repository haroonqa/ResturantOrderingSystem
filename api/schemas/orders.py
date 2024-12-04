from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class OrderBase(BaseModel):
    customer_id: int
    order_details: list[OrderDetail] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    pass


class Order(OrderBase):
    id: int
    order_completed: Optional[bool] = False
    order_date: Optional[datetime] = None
    

    class ConfigDict:
        from_attributes = True
