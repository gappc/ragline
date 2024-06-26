import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    roles = Column(String)
    is_active = Column(Boolean, default=True)

    chat_sessions = relationship("ChatSession", back_populates="user")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True)
    chat_session_id = Column(String, index=True, unique=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="chat_sessions")

    chat_events = relationship("ChatEvent", back_populates="chat_session")


class ChatEvent(Base):
    __tablename__ = "chat_events"

    id = Column(Integer, primary_key=True)
    chat_session_id = Column(
        String, ForeignKey("chat_sessions.chat_session_id"), index=True
    )
    query_id = Column(String)
    content = Column(String)
    type = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    chat_session = relationship("ChatSession", back_populates="chat_events")
