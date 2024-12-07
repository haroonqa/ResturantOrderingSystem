from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..dependencies.database import get_db
from ..schemas.ratings_reviews import RatingsReviewsCreate, RatingsReviewsResponse
from ..models.ratings_reviews import RatingsReviews
from ..models.menu_items import MenuItem
from ..models.customer import Customer

router = APIRouter(
    tags=["Ratings and Reviews"],
    prefix="/ratings_reviews"
)

@router.post("/", response_model=RatingsReviewsResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: RatingsReviewsCreate, db: Session = Depends(get_db)):
    # Check if the menu item exists
    menu_item = db.query(MenuItem).filter(MenuItem.id == review.menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Check if the customer exists
    customer = db.query(Customer).filter(Customer.id == review.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    new_review = RatingsReviews(
        review_text=review.review_text,
        rating=review.rating,
        menu_item_id=review.menu_item_id,
        customer_id=review.customer_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/", response_model=List[RatingsReviewsResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    reviews = db.query(RatingsReviews).all()
    return reviews

@router.get("/{review_id}", response_model=RatingsReviewsResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(RatingsReviews).filter(RatingsReviews.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=RatingsReviewsResponse)
def update_review(review_id: int, updated_review: RatingsReviewsCreate, db: Session = Depends(get_db)):
    review = db.query(RatingsReviews).filter(RatingsReviews.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.review_text = updated_review.review_text
    review.rating = updated_review.rating
    review.menu_item_id = updated_review.menu_item_id
    review.customer_id = updated_review.customer_id
    db.commit()
    db.refresh(review)
    return review

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(RatingsReviews).filter(RatingsReviews.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    db.delete(review)
    db.commit()
    return {"detail": "Review deleted successfully"}
