from pydantic import BaseModel
from typing import Optional


class IngredientBase(BaseModel):
    min_threshold: Optional[int] = 10
    low_stock_alert: Optional[bool] = False

class IngredientCreate(IngredientBase):
    name: str
    quantity: int
    unit: str

class IngredientUpdate(IngredientBase):
    name: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None

class IngredientResponse(IngredientBase):
    id: int
    name: str
    quantity: int
    unit: str

    class Config:
        from_attributes = True