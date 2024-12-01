from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import customer as model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from ..schemas import customer


def create(db: Session, request):
    new_customer = model.Customer(
        name=request.name,
        email=request.email,
        phone_number=request.phone_number,
        address=request.address,
        password=request.password

    )

    try:
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_customer

def read_all(db: Session):
    try:
        result = db.query(model.Customer).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, customer_id):
    try:
        customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return customer


def update(db: Session, customer_id, request):
    try:
        customer = db.query(model.Customer).filter(model.Customer.id == customer_id)
        if not customer.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        customer.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return customer.first()


def delete(db: Session, customer_id):
    try:
        customer = db.query(model.Customer).filter(model.Customer.id == customer_id)
        if not customer.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        customer.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# this function is being used for guest creation

def create_guest(db: Session, guest_create: customer.GuestCreate):
    # base name for guest accounts
    base_name = "Guest"
    guest_name = base_name
    suffix = 0

    # Ensure the name is unique by adding a number to end of it ex after guest, guest1,guest2......
    while db.query(model.Customer).filter_by(name=guest_name).first():
        suffix += 1
        guest_name = f"{base_name}{suffix}"

    # Create the guest customer with a unique name
    guest_customer = model.Customer(
        name=guest_name,  # Dynamically determined unique name
        email=guest_create.email,
        phone_number=guest_create.phone_number,
    )
    db.add(guest_customer)
    db.commit()
    db.refresh(guest_customer)
    return guest_customer

def update_guest(db: Session, guest_id, request):
    try:
        # Use 'like' to match names like 'Guest', 'Guest1', 'Guest2', etc.
        guest = db.query(model.Customer).filter(
            model.Customer.id == guest_id,
            model.Customer.name.like("Guest%")  # Correct pattern matching
        )
        if not guest.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest Id not found!")

        # Update the guest with new data
        update_data = request.dict(exclude_unset=True)
        guest.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return guest.first()

def delete_guest(db: Session, guest_id):
    try:
        guest = db.query(model.Customer).filter(model.Customer.id == guest_id, model.Customer.name.like("Guest%"))
        if not guest.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest Id not found!")
        guest.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def read_all_guests(db: Session):
    try:
        result = db.query(model.Customer).filter(model.Customer.name.like("Guest%")).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one_guest(db: Session, guest_id):
    try:
        guest = db.query(model.Customer).filter(model.Customer.id == guest_id, model.Customer.name.like("Guest%")).first()
        if not guest:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guest Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return guest