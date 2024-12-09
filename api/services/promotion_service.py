from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from ..models.promotion import Promotion


def apply_promotion_to_order(db: Session, promotion_code: str, order_total: float) -> float:
    """
    Apply a promotion code to an order and return the discounted total.
    """
    promotion = db.query(Promotion).filter(Promotion.code == promotion_code).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion code not found")
    
    if not promotion.is_active:
        raise HTTPException(status_code=400, detail="Promotion code is not active")
    
    if promotion.expiration_date < datetime.now():
        raise HTTPException(status_code=400, detail="Promotion code has expired")
    
    discount_amount = order_total * (promotion.discount_percentage / 100)
    discounted_total = order_total - discount_amount
    
    return discounted_total