import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.promotion import Promotion
from ..services.promotion_service import apply_promotion_to_order
from fastapi import HTTPException

@pytest.fixture
def db_session(mocker):
    """Mock database session"""
    return mocker.Mock(spec=Session)

@pytest.fixture
def sample_promotions():
    """Create sample promotions for testing"""
    current_time = datetime.now()
    return [
        Promotion(
            id=1,
            code="SAVE10",
            discount_percentage=10,
            expiration_date=current_time + timedelta(days=30),
            is_active=True
        ),
        Promotion(
            id=2,
            code="EXPIRED20",
            discount_percentage=20,
            expiration_date=current_time - timedelta(days=1),
            is_active=True
        ),
        Promotion(
            id=3,
            code="FUTURE15",
            discount_percentage=15,
            expiration_date=current_time + timedelta(days=30),
            is_active=False
        )
    ]

def test_create_promotion(db_session):
    """Test creating a new promotion"""
    # Arrange
    current_time = datetime.now()
    promotion_data = {
        "code": "NEWPROMO",
        "discount_percentage": 25,
        "expiration_date": current_time + timedelta(days=30),
        "is_active": True
    }
    
    # Act
    promotion = Promotion(**promotion_data)
    db_session.add(promotion)
    db_session.commit()
    
    # Assert
    assert promotion.code == "NEWPROMO"
    assert promotion.discount_percentage == 25
    assert promotion.is_active is True
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()

def test_apply_valid_promotion(db_session, sample_promotions):
    """Test applying a valid promotion code"""
    # Arrange
    promotion = sample_promotions[0]  # SAVE10
    db_session.query.return_value.filter.return_value.first.return_value = promotion
    order_total = 100.00
    
    # Act
    discounted_total = apply_promotion_to_order(db_session, "SAVE10", order_total)
    
    # Assert
    assert discounted_total == 90.00  # 10% off 100

def test_apply_expired_promotion(db_session, sample_promotions):
    """Test applying an expired promotion code"""
    # Arrange
    promotion = sample_promotions[1]  # EXPIRED20
    db_session.query.return_value.filter.return_value.first.return_value = promotion
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        apply_promotion_to_order(db_session, "EXPIRED20", 100.00)
    assert exc.value.status_code == 400
    assert "expired" in str(exc.value.detail).lower()

def test_apply_inactive_promotion(db_session, sample_promotions):
    """Test applying an inactive promotion code"""
    # Arrange
    promotion = sample_promotions[2]  # FUTURE15
    db_session.query.return_value.filter.return_value.first.return_value = promotion
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        apply_promotion_to_order(db_session, "FUTURE15", 100.00)
    assert exc.value.status_code == 400
    assert "not active" in str(exc.value.detail).lower()

def test_invalid_promotion_code(db_session):
    """Test applying a non-existent promotion code"""
    # Arrange
    db_session.query.return_value.filter.return_value.first.return_value = None
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        apply_promotion_to_order(db_session, "INVALID", 100.00)
    assert exc.value.status_code == 404

def test_deactivate_promotion(db_session, sample_promotions):
    """Test deactivating a promotion"""
    # Arrange
    promotion = sample_promotions[0]
    db_session.query.return_value.filter.return_value.first.return_value = promotion
    
    # Act
    promotion.is_active = False
    db_session.commit()
    
    # Assert
    assert promotion.is_active is False
    db_session.commit.assert_called_once()

def test_update_promotion_expiration(db_session, sample_promotions):
    """Test updating promotion expiration"""
    # Arrange
    promotion = sample_promotions[0]
    db_session.query.return_value.filter.return_value.first.return_value = promotion
    new_expiration_date = datetime.now() + timedelta(days=60)
    
    # Act
    promotion.expiration_date = new_expiration_date
    db_session.commit()
    
    # Assert
    assert promotion.expiration_date == new_expiration_date
    db_session.commit.assert_called_once()
