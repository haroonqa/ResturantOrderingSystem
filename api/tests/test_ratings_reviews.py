import pytest
from sqlalchemy.orm import Session
from ..models.ratings_reviews import RatingsReviews
from ..models.menu_items import MenuItem
from ..models.customer import Customer
from fastapi import HTTPException

@pytest.fixture
def db_session(mocker):
    """Mock database session"""
    return mocker.Mock(spec=Session)

@pytest.fixture
def sample_customer():
    """Create a sample customer for testing"""
    return Customer(
        name="Test Customer",
        email="test@example.com",
        phone_number="1234567890",
        address="123 Test St"
    )

@pytest.fixture
def sample_menu_item():
    """Create a sample menu item for testing"""
    return MenuItem(
        id=1,
        name="Test Pizza",
        price=10.99,
        calories=800,
        category="Pizza"
    )

def test_create_review(db_session, sample_customer, sample_menu_item):
    """Test creating a new review"""
    # Arrange
    review_data = {
        "menu_item_id": sample_menu_item.id,
        "customer_id": sample_customer.id,
        "rating": 5,
        "review_text": "Great pizza!"
    }
    
    # Mock the database queries
    db_session.query.return_value.filter.return_value.first.side_effect = [
        sample_menu_item,  # For menu item check
        sample_customer,   # For customer check
        None              # For duplicate check
    ]
    
    # Act
    review = RatingsReviews(**review_data)
    db_session.add(review)
    db_session.commit()
    
    # Assert
    assert review.rating == 5
    assert review.review_text == "Great pizza!"
    assert review.menu_item_id == sample_menu_item.id
    assert review.customer_id == sample_customer.id
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()

def test_invalid_rating_value(db_session, sample_customer, sample_menu_item):
    """Test that invalid rating values are rejected"""
    # Arrange
    review_data = {
        "menu_item_id": sample_menu_item.id,
        "customer_id": sample_customer.id,
        "rating": 6,  # Invalid rating > 5
        "review_text": "Great pizza!"
    }
    
    # Act & Assert
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        RatingsReviews(**review_data)

def test_get_menu_item_reviews(db_session, sample_menu_item):
    """Test retrieving all reviews for a menu item"""
    # Arrange
    reviews = [
        RatingsReviews(menu_item_id=1, customer_id=1, rating=5, review_text="Great!"),
        RatingsReviews(menu_item_id=1, customer_id=2, rating=4, review_text="Good!")
    ]
    db_session.query.return_value.filter.return_value.all.return_value = reviews
    
    # Act
    result = db_session.query(RatingsReviews).filter(
        RatingsReviews.menu_item_id == sample_menu_item.id
    ).all()
    
    # Assert
    assert len(result) == 2
    assert result[0].rating == 5
    assert result[1].rating == 4

def test_update_review(db_session):
    """Test updating an existing review"""
    # Arrange
    existing_review = RatingsReviews(
        menu_item_id=1,
        customer_id=1,
        rating=3,
        review_text="Original review"
    )
    db_session.query.return_value.filter.return_value.first.return_value = existing_review
    
    # Act
    existing_review.rating = 4
    existing_review.review_text = "Updated review"
    db_session.commit()
    
    # Assert
    assert existing_review.rating == 4
    assert existing_review.review_text == "Updated review"
    db_session.commit.assert_called_once()

def test_delete_review(db_session):
    """Test deleting a review"""
    # Arrange
    existing_review = RatingsReviews(
        menu_item_id=1,
        customer_id=1,
        rating=3,
        review_text="To be deleted"
    )
    db_session.query.return_value.filter.return_value.first.return_value = existing_review
    
    # Act
    db_session.delete(existing_review)
    db_session.commit()
    
    # Assert
    db_session.delete.assert_called_once_with(existing_review)
    db_session.commit.assert_called_once()
