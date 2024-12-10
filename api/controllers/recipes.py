from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import recipes as model
from sqlalchemy.exc import SQLAlchemyError
from ..dependencies.database import get_db
from ..schemas import recipes


def create_recipe(db: Session, request: recipes.RecipeCreate):
    new_recipe = model.Recipe(
        sandwich_id=request.sandwich_id,
        ingredients_needed=request.ingredients_needed or model.Recipe.default_ingredient_list
    )
    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_recipe


def get_all_recipes(db: Session):
    try:
        result = db.query(model.Recipe).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def get_recipe(recipe_id: int, db: Session):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return recipe


def update_recipe(recipe_id: int, request: recipes.RecipeUpdate, db: Session):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        if not recipe.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

        update_data = request.dict(exclude_unset=True)
        recipe.update(update_data, synchronize_session=False)
        db.commit()

    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return recipe.first()


def delete_recipe(db: Session, recipe_id: int):
    try:
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        if not recipe.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        recipe.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
