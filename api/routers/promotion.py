from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.promotion import PromotionCreate, Promotion, PromotionUpdate
from ..controllers import promotion as controller
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Promotion"],
    prefix="/promotion"
)

@router.post("/", response_model=Promotion)
def create_promotion_route(request: PromotionCreate, db: Session = Depends(get_db)):
    return controller.create_promotion(db, request)

@router.get("/", response_model=list[Promotion])
def read_all_promotions(db: Session = Depends(get_db)):
    return controller.get_all_promotion(db)

@router.get("/{code}", response_model=Promotion)
def read_promotion_by_code(code: str, db: Session = Depends(get_db)):
    return controller.get_promotion_by_code(db, code)

@router.put("/{promotion_id}", response_model=Promotion)
def update_promotion_route(promotion_id: int, request: PromotionUpdate, db: Session = Depends(get_db)):
    return controller.update_promotion(db, promotion_id, request)

@router.delete("/{promotion_id}", status_code=controller.status.HTTP_204_NO_CONTENT)
def delete_promotion_route(promotion_id: int, db: Session = Depends(get_db)):
    controller.delete_promotion(db, promotion_id)
    return controller.HTTPException(status_code=controller.status.HTTP_204_NO_CONTENT)
