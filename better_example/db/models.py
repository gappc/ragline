from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    roles = Column(String)
    is_active = Column(Boolean, default=True)

    # items = relationship("Conversation", back_populates="owner")


# class Conversation(Base):
#     __tablename__ = "conversations"

#     id = Column(Integer, primary_key=True)
#     title = Column(String, index=True)
#     description = Column(Text)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
