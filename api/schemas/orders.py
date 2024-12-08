from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class OrderBase(BaseModel):
    customer_id: int
    order_completed: Optional[bool] = False

class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    

    class ConfigDict:
        from_attributes = True
