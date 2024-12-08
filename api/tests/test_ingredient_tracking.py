import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.ingredients import Ingredient
from ..models.menu_items import MenuItem
from ..services.ingredient_tracking import (
    check_and_update_ingredients,
    get_low_stock_ingredients,
    restock_ingredient,
    InsufficientIngredientsError
)
from sqlalchemy import and_

@pytest.fixture
def db_session(mocker):
    """Mock database session"""
    return mocker.Mock(spec=Session)

@pytest.fixture
def sample_menu_item(mocker):
    """Create a sample menu item with ingredients"""
    menu_item = MenuItem(
        id=1,
        name="Test Pizza",
        price=10.99,
        calories=800,
        category="Pizza"
    )
    menu_item.ingredients = [
        Ingredient(
            id=1,
            name="Tomato",
            quantity=100,
            min_threshold=20,
            unit="pieces"
        ),
        Ingredient(
            id=2,
            name="Cheese",
            quantity=5,
            min_threshold=10,
            unit="kg"
        )
    ]
    return menu_item

@pytest.fixture
def sample_ingredients():
    """Create sample ingredients for testing"""
    return [
        Ingredient(
            name="Tomato",
            quantity=100,
            min_threshold=20,
            unit="pieces",
            low_stock_alert=True
        ),
        Ingredient(
            name="Cheese",
            quantity=5,
            min_threshold=10,
            unit="kg",
            low_stock_alert=True
        ),
        Ingredient(
            name="Flour",
            quantity=50,
            min_threshold=30,
            unit="kg",
            low_stock_alert=True
        )
    ]

def test_check_sufficient_ingredients(db_session, sample_menu_item):
    """Test checking ingredients with sufficient quantity"""
    # Arrange
    db_session.query.return_value.filter.return_value.first.return_value = sample_menu_item
    
    # Act
    result = check_and_update_ingredients(db_session, menu_item_id=1, quantity=5)
    
    # Assert
    assert result is True
    assert sample_menu_item.ingredients[0].quantity == 95  # Tomato decreased by 5
    db_session.commit.assert_called_once()

def test_check_insufficient_ingredients(db_session, sample_menu_item):
    """Test checking ingredients with insufficient quantity"""
    # Arrange
    sample_menu_item.ingredients[1].quantity = 5  # Cheese with low quantity
    db_session.query.return_value.filter.return_value.first.return_value = sample_menu_item
    
    # Act & Assert
    with pytest.raises(InsufficientIngredientsError):
        check_and_update_ingredients(db_session, menu_item_id=1, quantity=10)

def test_get_low_stock_ingredients(db_session, sample_ingredients):
    """Test getting ingredients below minimum threshold"""
    # Arrange
    db_session.query.return_value.filter.return_value.all.return_value = [
        sample_ingredients[1]  # Only Cheese is below threshold
    ]
    
    # Act
    low_stock = get_low_stock_ingredients(db_session)
    
    # Assert
    assert len(low_stock) == 1
    assert low_stock[0]["name"] == "Cheese"
    assert low_stock[0]["current_quantity"] == 5
    assert low_stock[0]["min_threshold"] == 10

def test_restock_ingredient(db_session, sample_ingredients):
    """Test restocking an ingredient"""
    # Arrange
    ingredient = sample_ingredients[1]  # Cheese with quantity 5
    db_session.query.return_value.filter.return_value.first.return_value = ingredient
    
    # Act
    restock_ingredient(db_session, ingredient_id=2, quantity=15)
    
    # Assert
    assert ingredient.quantity == 20  # 5 + 15
    db_session.commit.assert_called_once()

def test_restock_invalid_quantity(db_session, sample_ingredients):
    """Test restocking with invalid quantity"""
    # Arrange
    ingredient = sample_ingredients[0]
    db_session.query.return_value.filter.return_value.first.return_value = ingredient
    
    # Act & Assert
    with pytest.raises(ValueError, match="Restock quantity must be positive"):
        restock_ingredient(db_session, ingredient_id=1, quantity=-5)

def test_ingredient_not_found(db_session):
    """Test handling non-existent ingredient"""
    # Arrange
    db_session.query.return_value.filter.return_value.first.return_value = None
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        restock_ingredient(db_session, ingredient_id=999, quantity=10)
    assert exc.value.status_code == 404

def test_update_min_threshold(db_session, sample_ingredients):
    """Test updating minimum threshold"""
    # Arrange
    ingredient = sample_ingredients[0]
    db_session.query.return_value.filter.return_value.first.return_value = ingredient
    
    # Act
    ingredient.min_threshold = 30
    db_session.commit()
    
    # Assert
    assert ingredient.min_threshold == 30
    db_session.commit.assert_called_once()
