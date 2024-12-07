from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models.orders import Order 
from sqlalchemy.exc import SQLAlchemyError
from ..services.ingredient_tracking import check_and_update_ingredients, InsufficientIngredientsError


def create(db: Session, request):
    try:
        for order_item in request.order_details:
            try:
                check_and_update_ingredients(
                    db, 
                    menu_item_id=order_item.menu_item_id,
                    quantity=order_item.quantity
                )
            except InsufficientIngredientsError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
        
        new_item = Order(
            customer_id=request.customer_id,
            promotion_id=request.promotion_id if hasattr(request, 'promotion_id') else None
        )
        
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


def read_one(db: Session, item_id):
    try:
        item = db.query(Order).filter(Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(Order).filter(Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
            
        update_data = {}
        if hasattr(request, 'customer_id'):
            update_data['customer_id'] = request.customer_id
        if hasattr(request, 'promotion_id'):
            update_data['promotion_id'] = request.promotion_id
            
        if update_data:
            item.update(update_data, synchronize_session=False)
            db.commit()
            
        return item.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def delete(db: Session, item_id):
    try:
        item = db.query(Order).filter(Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
