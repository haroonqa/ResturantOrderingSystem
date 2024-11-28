from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str
    quantity: int
    unit: str

class IngredientCreate(IngredientBase):
    pass

class IngredientResponse(IngredientBase):
    id: int

    class Config:
        orm_mode = True