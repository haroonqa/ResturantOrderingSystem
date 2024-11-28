from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    price: float
    calories: int
    category: str

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        orm_mode = True
