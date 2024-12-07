from pydantic import BaseModel
from typing import Optional


class IngredientBase(BaseModel):
    name: str
    quantity: int
    unit: str
    min_threshold: Optional[int] = 10
    low_stock_alert: Optional[bool] = False

class IngredientCreate(IngredientBase):
    pass

class IngredientResponse(IngredientBase):
    id: int

    class Config:
        from_attributes = True