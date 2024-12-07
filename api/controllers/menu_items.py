from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.menu_items import MenuItem
from ..schemas.menu_items import MenuItemCreate


def create_menu_item(db: Session, request: MenuItemCreate):
    new_item = MenuItem(**request.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_all_menu_items(db: Session):
    return db.query(MenuItem).all()


def get_menu_item_by_id(db: Session, menu_item_id: int):
    item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    return item


def update_menu_item(db: Session, menu_item_id: int, request: MenuItemCreate):
    item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    for key, value in request.dict().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def delete_menu_item(db: Session, menu_item_id: int):
    item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    db.delete(item)
    db.commit()
