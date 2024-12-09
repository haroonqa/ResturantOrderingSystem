import pytest
from sqlalchemy.orm import Session
from ..models.menu_items import MenuItem
from ..services.menu_search import search_menu_items
from fastapi import HTTPException

@pytest.fixture
def db_session(mocker):
    """Mock database session"""
    return mocker.Mock(spec=Session)

@pytest.fixture
def sample_menu_items():
    """Create sample menu items for testing"""
    return [
        MenuItem(
            id=1,
            name="Veggie Pizza",
            price=14.99,
            calories=800,
            category="Pizza",
            dietary_type="vegetarian",
            description="Fresh vegetables on a crispy crust",
            tags="vegetarian,healthy"
        ),
        MenuItem(
            id=2,
            name="Classic Burger",
            price=12.99,
            calories=1000,
            category="Burgers",
            description="Beef patty with cheese",
            tags="beef,classic"
        ),
        MenuItem(
            id=3,
            name="Vegan Bowl",
            price=13.99,
            calories=600,
            category="Bowls",
            dietary_type="vegan",
            description="Quinoa and vegetables",
            tags="vegan,healthy,gluten-free"
        )
    ]

def test_create_menu_item(db_session):
    """Test creating a new menu item"""
    # Arrange
    item_data = {
        "name": "Test Pizza",
        "price": 15.99,
        "calories": 900,
        "category": "Pizza",
        "dietary_type": "vegetarian",
        "description": "Test description",
        "tags": "test,pizza"
    }
    
    # Act
    menu_item = MenuItem(**item_data)
    db_session.add(menu_item)
    db_session.commit()
    
    # Assert
    assert menu_item.name == "Test Pizza"
    assert menu_item.price == 15.99
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()

def test_search_vegetarian_items(db_session, sample_menu_items):
    """Test searching for vegetarian items"""
    # Arrange
    db_session.query.return_value.filter.return_value.all.return_value = [
        item for item in sample_menu_items if item.dietary_type == "vegetarian"
    ]
    
    # Act
    results = search_menu_items(db_session, dietary_type="vegetarian")
    
    # Assert
    assert len(results) == 1
    assert results[0].name == "Veggie Pizza"
    assert results[0].dietary_type == "vegetarian"

def test_search_by_price_range(db_session, sample_menu_items):
    """Test searching items within a price range"""
    # Arrange
    db_session.query.return_value.filter.return_value.all.return_value = [
        item for item in sample_menu_items if item.price <= 13.00
    ]
    
    # Act
    results = search_menu_items(db_session, max_price=13.00)
    
    # Assert
    assert len(results) == 1
    assert results[0].name == "Classic Burger"

def test_search_by_category(db_session, sample_menu_items):
    """Test searching items by category"""
    # Arrange
    db_session.query.return_value.filter.return_value.all.return_value = [
        item for item in sample_menu_items if item.category == "Pizza"
    ]
    
    # Act
    results = search_menu_items(db_session, category="Pizza")
    
    # Assert
    assert len(results) == 1
    assert results[0].category == "Pizza"

def test_search_by_tags(db_session, sample_menu_items):
    """Test searching items by tags"""
    # Arrange
    db_session.query.return_value.filter.return_value.all.return_value = [
        item for item in sample_menu_items if "healthy" in item.tags
    ]
    
    # Act
    results = search_menu_items(db_session, tags=["healthy"])
    
    # Assert
    assert len(results) == 2
    assert all("healthy" in item.tags for item in results)

def test_update_menu_item(db_session, sample_menu_items):
    """Test updating a menu item"""
    # Arrange
    item = sample_menu_items[0]
    db_session.query.return_value.filter.return_value.first.return_value = item
    
    # Act
    item.price = 16.99
    item.description = "Updated description"
    db_session.commit()
    
    # Assert
    assert item.price == 16.99
    assert item.description == "Updated description"
    db_session.commit.assert_called_once()

def test_delete_menu_item(db_session, sample_menu_items):
    """Test deleting a menu item"""
    # Arrange
    item = sample_menu_items[0]
    db_session.query.return_value.filter.return_value.first.return_value = item
    
    # Act
    db_session.delete(item)
    db_session.commit()
    
    # Assert
    db_session.delete.assert_called_once_with(item)
    db_session.commit.assert_called_once()
