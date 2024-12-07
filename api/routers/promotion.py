from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.promotion import PromotionCreate, Promotion
from ..controllers.promotion import create_promotion, get_all_promotion
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Promotion"],
    prefix="/promotion"
)

@router.post("/", response_model=Promotion)
def create_promotion_route(request: PromotionCreate, db: Session = Depends(get_db)):
    return create_promotion(db, request)

@router.get("/", response_model=list[Promotion])
def get_all_promotion_route(db: Session = Depends(get_db)):
    return get_all_promotion(db)
