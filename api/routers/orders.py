from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{order_id}", response_model=schema.Order)
def read_one(order_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, order_id=order_id)


@router.put("/{order_id}", response_model=schema.Order)
def update(order_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, order_id=order_id)


@router.delete("/{order_id}")
def delete(order_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, order_id=order_id)

@router.get("/{order_id}/status", response_model=str)
def get_order_status(order_id: int, db: Session = Depends(get_db)):
    return controller.get_order_status(db=db, order_id=order_id)

#endpoint to get orders based on a date range
@router.get("/date-range/input date as MM/DD/YYYY")
def get_orders_by_date_range(start_date: str, end_date: str, db: Session = Depends(get_db)):
        return controller.read_by_date_range(db, start_date, end_date)

@router.get("/revenue-by-date/")
def get_revenue_by_date(order_date: str, db: Session = Depends(get_db)):
    """
    Retrieves the total revenue for all transactions associated with orders placed on a specific date.
    """
    return controller.get_revenue_by_date(db, order_date)
