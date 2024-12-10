from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models.orders import Order
from ..models.transactions import Transaction
from sqlalchemy.exc import SQLAlchemyError
from ..services.ingredient_tracking import check_and_update_ingredients, InsufficientIngredientsError
from datetime import datetime
from sqlalchemy import and_




def create(db: Session, request):
    new_item = Order(
        customer_id = request.customer_id,
        order_completed = request.order_completed
        )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        return new_item
        
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_all(db: Session):
    try:
        result = db.query(Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, order_id):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def update(db: Session, order_id, request):
    try:
        order = db.query(Order).filter(Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
        update_data = request.dict(exclude_unset=True)
        order.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order.first()


def delete(db: Session, order_id):
    try:
        order = db.query(Order).filter(Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        order.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# date range function ot get the orders pplaced by date
def read_by_date_range(db: Session, start_date: str, end_date: str):
    try:
        # Parse the date strings into datetime objects
        start = datetime.strptime(start_date, '%m/%d/%Y')
        end = datetime.strptime(end_date, '%m/%d/%Y')

        # Query the database for orders within the date range
        orders = db.query(Order).filter(
            and_(
                Order.order_date >= start,
                Order.order_date <= end
            )
        ).all()

        if not orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No orders found in the specified date range"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Please use MM/DD/YYYY."
        )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return orders


def get_order_status(db: Session, order_id: int):
    try:
        # Query the order based on the given order_id
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        # Return the status of the order (e.g., completed or pending)
        return "Completed" if order.order_completed else "Pending"
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def get_revenue_by_date(db: Session, order_date: str):
    try:
        revenue = 0

        orders = read_by_date_range(db, order_date, order_date) #THIS MAY CAUSE ISSUES

        for order in orders:
            order_id = order.id
            transaction = db.query(Transaction).filter(Transaction.order_id == order_id).first()
            revenue += transaction.price

        return {
            "order_date": order_date,
            "total_revenue": revenue,
            "transactions_count": len(orders)
        }
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Please use MM/DD/YYYY."
        )
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
