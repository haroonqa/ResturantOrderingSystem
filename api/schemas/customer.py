from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str

class CustomerCreate(CustomerBase):
        password: str

class CustomerUpdate(BaseModel):
    name: str = None
    email: Optional[str] = None 
    phone_number: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None

class CustomerLogin(BaseModel):
        email: str
        password: str

class Customer(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True