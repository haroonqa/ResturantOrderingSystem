from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class PromotionBase(BaseModel):
    code: Optional[str] = Field(..., max_length=50, description="Unique promotion code")
    description: Optional[str] | None = Field(None, max_length=255, description="Details about the promotion")
    discount_percentage: Optional[int] = Field(..., ge=0, le=100, description="Discount percentage for the promotion")
    expiration_date: Optional[date] = Field(..., description="Expiration date of the promotion")
    is_active: Optional[bool] = Field(default=True, description="Whether the promotion is currently active")

    class Config:
        from_attributes = True  

class PromotionCreate(PromotionBase):
    code: str = Field(..., max_length=50, description="Unique promotion code")
    description: str | None = Field(None, max_length=255, description="Details about the promotion")
    discount_percentage: int = Field(..., ge=0, le=100, description="Discount percentage for the promotion")
    is_active: bool = Field(default=True, description="Whether the promotion is currently active")


class PromotionUpdate(PromotionBase):
    code: Optional[str] = Field(..., max_length=50, description="Unique promotion code")
    description: Optional[str] | None = Field(None, max_length=255, description="Details about the promotion")
    discount_percentage: Optional[int] = Field(..., ge=0, le=100, description="Discount percentage for the promotion")
    expiration_date: Optional[date] = Field(..., description="Expiration date of the promotion")
    is_active: Optional[bool] = Field(default=True, description="Whether the promotion is currently active")

class Promotion(PromotionBase):
    id: int

    class Config:
        from_attributes = True
