from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.promotion import PromotionCreate
from ..models.promotion import Promotion
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Promotion"],
    prefix="/promotion"
)


# POST endpoint to create a promotion
@router.post("/", response_model=PromotionCreate)
def create_promotion(request: PromotionCreate, db: Session = Depends(get_db)):
    # Save the promotion to the database
    new_promotion = Promotion(
        code=request.code,
        description=request.description,
        discount_percentage=request.discount_percentage,
        expiration_date=request.expiration_date,
        is_active=request.is_active
    )
    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)
    return new_promotion


# GET endpoint to fetch all promotions
@router.get("/", response_model=list[PromotionCreate])
def get_all_promotions(db: Session = Depends(get_db)):
    return db.query(Promotion).all()
