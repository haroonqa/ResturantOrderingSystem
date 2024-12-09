from pydantic import BaseModel, Field
from typing import Optional

class RatingsReviewsBase(BaseModel):
    review_text: Optional[str] = None
    rating: int = Field(ge=1, le=5, description="Rating must be between 1 and 5")

class RatingsReviewsCreate(RatingsReviewsBase):
    menu_item_id: int
    customer_id: int

class RatingsReviewsResponse(RatingsReviewsBase):
    id: int
    menu_item_id: int
    customer_id: int

    class Config:
        from_attributes = True