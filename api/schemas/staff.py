from pydantic import BaseModel
from typing import Optional


class StaffBase(BaseModel):
    username: str

class StaffCreate(StaffBase):
    pass

class StaffUpdate(StaffBase):
    pass

class StaffInDBBase(StaffBase):
    id: Optional[int] = None
    username: str

    class Config:
        from_attributes = True

