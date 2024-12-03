from pydantic import BaseModel
from typing import Optional


class MenuItemBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    pass  # Additional fields for creation can go here if needed


class MenuItem(MenuItemBase):
    id: int

    class Config:
        from_attributes = True
