from pydantic import BaseModel
from typing import Optional

class RatingsReviewsBase(BaseModel):
    review_text: Optional[str]
    rating: int

class RatingsReviewsCreate(RatingsReviewsBase):
    menu_item_id: int
    customer_id: int

class RatingsReviewsResponse(RatingsReviewsBase):
    id: int
    menu_item: dict
    customer: dict

    class Config:
        from_attributes = True