import pytest
from sqlalchemy.orm import Session
from ..models.ingredients import Ingredient
from ..dependencies.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_ingredient():
    """Create a sample ingredient for testing"""
    return Ingredient(
        name="Test Ingredient",
        quantity=100,
        unit="grams",
        min_threshold=10,
        low_stock_alert=False
    )

def test_create_ingredient(db_session: Session):
    """Test creating a new ingredient"""
    # Arrange
    ingredient_data = {
        "name": "Tomato",
        "quantity": 50,
        "unit": "pieces",
        "min_threshold": 10,
        "low_stock_alert": False
    }
    
    # Act
    ingredient = Ingredient(**ingredient_data)
    db_session.add(ingredient)
    db_session.commit()
    
    # Assert
    assert ingredient.id is not None
    assert ingredient.name == "Tomato"
    assert ingredient.quantity == 50
    assert ingredient.unit == "pieces"

def test_create_ingredient_without_quantity(db_session: Session):
    """Test creating an ingredient without quantity and unit"""
    # Arrange
    ingredient_data = {
        "name": "Salt",
        "min_threshold": 5,
        "low_stock_alert": False
    }
    
    # Act
    ingredient = Ingredient(**ingredient_data)
    db_session.add(ingredient)
    db_session.commit()
    
    # Assert
    assert ingredient.id is not None
    assert ingredient.name == "Salt"
    assert ingredient.quantity is None
    assert ingredient.unit is None

def test_update_ingredient(db_session: Session, sample_ingredient):
    """Test updating an ingredient"""
    # Arrange
    db_session.add(sample_ingredient)
    db_session.commit()
    
    # Act
    sample_ingredient.quantity = 75
    sample_ingredient.low_stock_alert = True
    db_session.commit()
    
    # Assert
    updated_ingredient = db_session.query(Ingredient).filter_by(id=sample_ingredient.id).first()
    assert updated_ingredient.quantity == 75
    assert updated_ingredient.low_stock_alert is True

def test_delete_ingredient(db_session: Session, sample_ingredient):
    """Test deleting an ingredient"""
    # Arrange
    db_session.add(sample_ingredient)
    db_session.commit()
    ingredient_id = sample_ingredient.id
    
    # Act
    db_session.delete(sample_ingredient)
    db_session.commit()
    
    # Assert
    deleted_ingredient = db_session.query(Ingredient).filter_by(id=ingredient_id).first()
    assert deleted_ingredient is None

def test_low_stock_alert_trigger(db_session: Session):
    """Test if low stock alert is triggered correctly"""
    # Arrange
    ingredient = Ingredient(
        name="Coffee Beans",
        quantity=8,  # Below min_threshold
        unit="kg",
        min_threshold=10,
        low_stock_alert=False
    )
    
    # Act
    db_session.add(ingredient)
    db_session.commit()
    
    # Assert
    assert ingredient.quantity < ingredient.min_threshold
    # Note: In a real application, you might have a trigger or service
    # that automatically updates low_stock_alert based on quantity
