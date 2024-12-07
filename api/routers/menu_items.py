from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..models.menu_items import MenuItem
from ..schemas.menu_items import MenuItemCreate, MenuItem
from ..controllers.menu_items import (
    create_menu_item,
    get_all_menu_items,
    get_menu_item_by_id,
    delete_menu_item
)
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Menu Items'],
    prefix="/menu_items"
)

@router.post("/", response_model=MenuItem)
def create_menu_item_route(request: MenuItemCreate, db: Session = Depends(get_db)):
    return create_menu_item(db=db, request=request)

@router.get("/", response_model=list[MenuItem])
def get_all_menu_items_route(db: Session = Depends(get_db)):
    return get_all_menu_items(db)

@router.get("/{menu_item_id}", response_model=MenuItem)
def get_menu_item_by_id_route(menu_item_id: int, db: Session = Depends(get_db)):
    return get_menu_item_by_id(db, menu_item_id=menu_item_id)

@router.delete("/{menu_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item_route(menu_item_id: int, db: Session = Depends(get_db)):
    delete_menu_item(db, menu_item_id=menu_item_id)
