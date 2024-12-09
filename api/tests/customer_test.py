from fastapi.testclient import TestClient
from ..controllers import customer as controller
from ..main import app
import pytest
from ..models import customer as model
from sqlalchemy.orm import Session
from ..schemas.customer import CustomerUpdate

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

def test_read_all(db_session):
    #create customer objects
    customer_data_1 = {
        "name": "Anthony Ramirez",
        "email": "anthony.ramirez@example.com",
        "phone_number": "0987654321",
        "address": "321 North Rd",
        "password": "NEWPassword"
    }

    customer_data_2 = {
        "name": "Moeez Awan",
        "email": "moeez.awan@example.com",
        "phone_number": "1234567890",
        "address": "123 South St",
        "password": "spassword"
    }

    customer_object_1 = model.Customer(**customer_data_1)
    customer_object_2 = model.Customer(**customer_data_2)


    # Call the create functions
    created_customer_1 = controller.create(db_session, customer_object_1)
    created_customer_2 = controller.create(db_session, customer_object_2)


    #assert obects were created
    assert created_customer_1 is not None
    assert created_customer_1.name == "Anthony Ramirez"
    assert created_customer_1.email == "anthony.ramirez@example.com"
    assert created_customer_1.phone_number == "0987654321"
    assert created_customer_1.address == "321 North Rd"
    assert created_customer_1.password == "NEWPassword"

    assert created_customer_2 is not None
    assert created_customer_2.name == "Moeez Awan"
    assert created_customer_2.email == "moeez.awan@example.com"
    assert created_customer_2.phone_number == "1234567890"
    assert created_customer_2.address == "123 South St"
    assert created_customer_2.password == "spassword"

    # Mock the behavior of `db_session.query().all()`
    db_session.query.return_value.all.return_value = [customer_object_1, customer_object_2]

    # Call the read_all function
    customers = controller.read_all(db_session)

    assert customers[0] is not None
    assert customers[0].name == "Anthony Ramirez"
    assert customers[0].email == "anthony.ramirez@example.com"
    assert customers[0].phone_number == "0987654321"
    assert customers[0].address == "321 North Rd"
    assert customers[0].password == "NEWPassword"

    assert customers[1] is not None
    assert customers[1].name == "Moeez Awan"
    assert customers[1].email == "moeez.awan@example.com"
    assert customers[1].phone_number == "1234567890"
    assert customers[1].address == "123 South St"
    assert customers[1].password == "spassword"

def test_read_one(db_session):
    #create customer objects
    customer_data_1 = {
        "name": "Anthony Ramirez",
        "email": "anthony.ramirez@example.com",
        "phone_number": "0987654321",
        "address": "321 North Rd",
        "password": "NEWPassword"
    }

    customer_data_2 = {
        "name": "Moeez Awan",
        "email": "moeez.awan@example.com",
        "phone_number": "1234567890",
        "address": "123 South St",
        "password": "spassword"
    }

    customer_object_1 = model.Customer(**customer_data_1)
    db_session.query.return_value.filter.return_value.first.return_value = customer_object_1
    customer_1 = controller.read_one(db_session, customer_id=1)

    assert customer_1 is not None
    assert customer_1.name == "Anthony Ramirez"
    assert customer_1.email == "anthony.ramirez@example.com"
    assert customer_1.phone_number == "0987654321"
    assert customer_1.address == "321 North Rd"
    assert customer_1.password == "NEWPassword"

    customer_object_2 = model.Customer(**customer_data_2)
    db_session.query.return_value.filter.return_value.first.return_value = customer_object_2
    customer_2 = controller.read_one(db_session, customer_id=2)

    assert customer_2 is not None
    assert customer_2.name == "Moeez Awan"
    assert customer_2.email == "moeez.awan@example.com"
    assert customer_2.phone_number == "1234567890"
    assert customer_2.address == "123 South St"
    assert customer_2.password == "spassword"









def test_update(db_session):
    #create customer objects
    customer_data_1 = {
        "name": "Anthony Ramirez",
        "email": "anthony.ramirez@example.com",
        "phone_number": "0987654321",
        "address": "321 North Rd",
        "password": "NEWPassword"
    }
    customer_object = model.Customer(**customer_data_1)
    db_session.query.return_value.filter.return_value.first.return_value = customer_object
    customer_1 = controller.read_one(db_session, customer_id=1)

    #assert creation of objects
    assert customer_1 is not None
    assert customer_1.name == "Anthony Ramirez"
    assert customer_1.email == "anthony.ramirez@example.com"
    assert customer_1.phone_number == "0987654321"
    assert customer_1.address == "321 North Rd"
    assert customer_1.password == "NEWPassword"

    #update object
    customer_data_2 = CustomerUpdate(
        name="Moeez Awan",
        email="moeez.awan@example.com",
        phone_number="1234567890",
        address="123 South St",
        password="spassword"
    )

    customer_updated = controller.update(db_session, customer_1.id, customer_data_2)

    customer_updated = controller.read_one(db_session, customer_id=customer_1.id)

    assert customer_updated is not None
    assert customer_updated.name == "Moeez Awan"
    assert customer_updated.email == "moeez.awan@example.com"
    assert customer_updated.phone_number == "1234567890"
    assert customer_updated.address == "123 South St"
    assert customer_updated.password == "spassword"
