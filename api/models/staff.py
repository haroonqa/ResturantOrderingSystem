from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from ..dependencies.database import Base

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)