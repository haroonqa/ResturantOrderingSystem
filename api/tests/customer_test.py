from fastapi.testclient import TestClient
from ..controllers import customers as controller
from ..main import app
import pytest
from ..models import customers as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_customer(db_session):
    # Create a sample customer
    customer_data = {
        "name": "Moeez Awan",
        "email": "moeez.awan@example.com",
        "phone_number": "1234567890",
        "address": "123 South St",
        "password": "spassword"
    }

    customer_object = model.Customer(**customer_data)

    # Call the create function
    created_customer = controller.create(db_session, customer_object)

    # Assertions
    assert created_customer is not None
    assert created_customer.name == "Moeez Awan"
    assert created_customer.email == "moeez.awan@example.com"
    assert created_customer.phone_number == "1234567890"
    assert created_customer.address == "123 South St"
    assert created_customer.password == "spassword"