from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(100), index=True, nullable=False)
    address = Column(String(100), index=True, nullable=False)
    password = Column(String(100), index=True, nullable=False)

    reviews = relationship("RatingsReviews", back_populates="customer")  


    def __init__(self, name, email, phone_number, address, password=None):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.password = password


    def createAccount(session,name, email, phone_number, address, password=None):
        while True:
            name = input("Please enter your name: ")
            email = input("Please enter your email: ")
            if "@" not in email or ".com" not in email:
                print("Please enter a valid email address")
                continue
            phone_number = input("Please enter your phone number (10 digits): ")
            if len(phone_number) != 10:
                print("Please make sure phone number is 10 digits")
                continue
            address = input("Please enter your address: ")
            password = input("Please enter a password for your account: ")
            if not (name and email and phone_number and address and password):
                print("Please make sure you are entering all fields")
                continue
            if session.query(Customer).filter((Customer.email == email) | (Customer.phone_number == phone_number)).first():
                print("It seems you already have an account")
                user_input = input("Please enter your email or phone number: ")
                print("Instructions to login are being sent to: " + user_input)
                return

            new_customer = Customer(
                name=name,
                email=email,
                phone_number=phone_number,
                address=address,
                password=password,
            )
            session.add(new_customer)
            session.commit()
            print("Account created successfully")
                           



