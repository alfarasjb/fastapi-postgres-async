from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from src.database import Base
from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    name: Optional[str] = None
    email: Optional[str] = None
    # created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.now()))
    # updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.now(), onupdate=datetime.now()))
