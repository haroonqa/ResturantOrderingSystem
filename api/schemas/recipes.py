from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from .sandwiches import Sandwich


class Ingredient(BaseModel):
    ingredient_id: int
    amount: int


class RecipeBase(BaseModel):
    sandwich_id: Optional[int] = None
    ingredients_needed: Optional[List[Dict[str, int]]] = Field(
        default=[
            {"ingredient_id": 1, "amount": 2},
            {"ingredient_id": 2, "amount": 2},
            {"ingredient_id": 3, "amount": 1}
        ],
        description="List of ingredients needed for the recipe"
    )


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    sandwich_id: Optional[int] = None
    ingredients_needed: Optional[List[Dict[str, int]]] = Field(
        default=[
            {"ingredient_id": 1, "amount": 2},
            {"ingredient_id": 2, "amount": 2},
            {"ingredient_id": 3, "amount": 1}
        ]
    )



class Recipe(RecipeBase):
    id: int

    class Config:
        orm_mode = True
