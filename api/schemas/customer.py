from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    email: str
    phone_number: str
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    password: str

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None 
    phone_number: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None

class CustomerLogin(BaseModel):
    email: str
    password: str

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True 

class GuestCreate(BaseModel):
    email: str
    phone_number: str
    address: str = "default_address" 
    password: str = "default_password"  # Provide a default value

class GuestResponse(BaseModel):
    id: int
    email: str
    phone_number: str

    class Config:
        from_attributes = True