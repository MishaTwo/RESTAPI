from enum import Enum
from .base import *
from sqlalchemy import Column, Integer, String, Float, Enum as Enum_SQLALCHEMY


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"User {self.name}"