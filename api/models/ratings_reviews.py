from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class RatingsReviews(Base):
    __tablename__ = 'ratings_reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(String(100), nullable=True)

    menu_item = relationship("MenuItem", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")  # Link back to Customer

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    def __init__(self, menu_item_id, customer_id, rating, review_text=None):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        self.menu_item_id = menu_item_id
        self.customer_id = customer_id
        self.rating = rating
        self.review_text = review_text
