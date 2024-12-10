from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..controllers import recipes as controller
from ..schemas import recipes as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Recipes'],
    prefix="/recipes"
)


@router.post("/", response_model=schema.Recipe)
def create_recipe(request: schema.RecipeCreate, db: Session = Depends(get_db)):
    return controller.create_recipe(db, request)


@router.get("/", response_model=list[schema.Recipe])
def get_all_recipes(db: Session = Depends(get_db)):
    return controller.get_all_recipes(db)


@router.get("/{recipe_id}", response_model=schema.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return controller.get_recipe(recipe_id, db)


@router.put("/{recipe_id}", response_model=schema.Recipe)
def update_recipe(recipe_id: int, request: schema.RecipeUpdate, db: Session = Depends(get_db)):
    return controller.update_recipe(recipe_id, request, db)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return controller.delete_recipe(db, recipe_id)
