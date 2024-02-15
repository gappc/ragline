from typing import List
from server.id import generate_id
from logger.custom_logger import logger
from server.hasher import Hasher
from sqlalchemy.orm import Session

from . import models, schemas


def create_chat_session(db: Session, user_id: str) -> models.ChatSession:
    chat_session_id = generate_id()

    db_chat_session = models.ChatSession(
        chat_session_id=chat_session_id,
        name="(No name)",
        owner_id=user_id,
    )
    db.add(db_chat_session)
    db.commit()
    db.refresh(db_chat_session)
    return db_chat_session


def get_chat_sessions(db: Session, user_id: int) -> List[models.ChatSession]:
    return (
        db.query(models.ChatSession)
        .filter(models.ChatSession.owner_id == user_id)
        .order_by(models.ChatSession.created_at)
        .all()
    )


def get_chat_session(
    db: Session, user_id: int, chat_session_id: str
) -> models.ChatSession | None:
    return (
        db.query(models.ChatSession)
        .filter(models.ChatSession.owner_id == user_id)
        .filter(models.ChatSession.chat_session_id == chat_session_id)
        .first()
    )


def create_chat_event(
    db: Session,
    user_id: int,
    chat_session_id: str,
    query_id: str,
    content: str,
    type: str,
) -> models.ChatEvent:
    throw_if_chat_session_not_found(db, user_id, chat_session_id)

    db_chat_evente = models.ChatEvent(
        chat_session_id=chat_session_id,
        query_id=query_id,
        content=content,
        type=type,
    )
    db.add(db_chat_evente)
    db.commit()
    return db_chat_evente


def get_chat_events(
    db: Session, user_id: int, chat_session_id: str
) -> List[models.ChatEvent]:
    throw_if_chat_session_not_found(db, user_id, chat_session_id)

    return (
        db.query(models.ChatEvent)
        .filter(models.ChatEvent.owner_id == chat_session_id)
        .order_by(models.ChatEvent.created_at)
        .all()
    )


def throw_if_chat_session_not_found(db: Session, user_id: int, chat_session_id: str):
    # get_chat_session will return None if chat session is not found
    # This includes a check if the chat session belongs to the user
    chat_session = get_chat_session(db, user_id, chat_session_id)
    if not chat_session:
        raise ValueError(f"Chat session {chat_session_id} not found")
