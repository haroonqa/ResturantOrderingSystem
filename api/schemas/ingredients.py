from pydantic import BaseModel
from typing import Optional


class IngredientBase(BaseModel):
    name: str
    quantity: int
    unit: str

class IngredientCreate(IngredientBase):
    pass

class IngredientResponse(IngredientBase):
    id: int

    class Config:
        from_attributes = True