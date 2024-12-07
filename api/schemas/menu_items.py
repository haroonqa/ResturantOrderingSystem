from pydantic import BaseModel
from typing import Optional, List


class MenuItemBase(BaseModel):
    name: str
    price: float
    calories: int
    category: str
    description: Optional[str] = None
    dietary_type: Optional[str] = None
    tags: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemFilter(BaseModel):
    category: Optional[str] = None
    dietary_type: Optional[str] = None
    max_price: Optional[float] = None
    max_calories: Optional[int] = None
    search_term: Optional[str] = None
    tags: Optional[List[str]] = None


class MenuItem(MenuItemBase):
    id: int

    class Config:
        from_attributes = True
