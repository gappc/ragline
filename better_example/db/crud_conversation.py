from server.id import generate_id
from logger.custom_logger import logger
from server.hasher import Hasher
from sqlalchemy.orm import Session

from . import models, schemas


def get_conversations(
    db: Session, user_id: int, conversation_id: str | None, type: str | None
):
    db_query = db.query(models.Conversation).filter(
        models.Conversation.owner_id == user_id
    )

    if conversation_id:
        db_query = db_query.filter(
            models.Conversation.conversation_id == conversation_id
        )

    if type:
        db_query = db_query.filter(models.Conversation.type == type)

    return db_query.order_by(models.Conversation.created_at).all()


def get_new_conversations(db: Session, user_id: int):
    return get_conversations(db, user_id, type="NEW")


def create_conversation(db: Session, user_id: str) -> models.Conversation:
    conversation_id = generate_id()
    return add_conversation(db, user_id, conversation_id, type="NEW")


def add_conversation(
    db: Session,
    user_id: str,
    conversation_id: str,
    type: str,
    query_id: str | None = None,
    content: str | None = None,
    refresh: bool = True,
) -> models.Conversation:
    db_conversation = models.Conversation(
        conversation_id=conversation_id,
        query_id=query_id,
        content=content,
        type=type,
        owner_id=user_id,
    )
    db.add(db_conversation)
    db.commit()
    if refresh:
        db.refresh(db_conversation)
    return db_conversation
