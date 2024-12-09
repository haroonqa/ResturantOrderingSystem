from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.promotion import Promotion
from ..schemas.promotion import PromotionCreate, PromotionUpdate


def create_promotion(db: Session, request: PromotionCreate):
    print(request.dict()) 

    new_promotion = Promotion(**request.dict())
    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)
    return new_promotion


def get_all_promotion(db: Session):
    return db.query(Promotion).all()


def get_promotion_by_code(db: Session, code: str):
    promotion = db.query(Promotion).filter(Promotion.code == code).first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    return promotion


def update_promotion(db: Session, promotion_id: int, request: PromotionUpdate):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    for key, value in request.dict().items():
        setattr(promotion, key, value)
    db.commit()
    db.refresh(promotion)
    return promotion


def delete_promotion(db: Session, promotion_id: int):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    db.delete(promotion)
    db.commit()
