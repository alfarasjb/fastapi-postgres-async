from sqlalchemy import (
    Column,
    Integer,
    String,
)

from src.database import Base
from sqlmodel import SQLModel, Field, Column
from typing import Optional

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)

"""
class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    name: Optional[str] = None
    email: Optional[str] = None
"""