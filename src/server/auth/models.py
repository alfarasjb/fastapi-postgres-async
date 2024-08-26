from src.database import Base

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    func,
    Enum,
    JSON,
    String,
    ForeignKey,
    UniqueConstraint,
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)