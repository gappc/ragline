from typing import Annotated

from db import models, schemas
from db.crud_chat_session import create_chat_session, get_chat_events, get_chat_sessions
from db.database import get_db
from fastapi import APIRouter, Depends
from logger.custom_logger import logger, logger_bind
from server.auth import RoleChecker, get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

allow_create_user = RoleChecker(["admin"])
allow_delete_user = RoleChecker(["admin"])


# Init new chat session
@router.post("/chat-sessions")
async def post_chat_session(
    user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    chat_session = create_chat_session(db, user.id)

    logger = logger_bind(chat_session.chat_session_id, None)
    logger.info(
        "Username: {} started new chat session with ID {}",
        user.username,
        chat_session.chat_session_id,
    )

    return chat_session


# Read chat sessions
@router.get("/chat-sessions", response_model=list[schemas.ChatSession])
async def read_chat_sessions(
    user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    chat_sessions = get_chat_sessions(db, user.id)

    logger.info(f"Found : {len(chat_sessions)} chat sessions")

    return chat_sessions


# Read chat events
@router.get("/chat-sessions/{chat_session_id}/events")
async def read_chat_events(
    user: Annotated[models.User, Depends(get_current_user)],
    chat_session_id: str,
    db: Session = Depends(get_db),
):
    chat_events = get_chat_events(db, user.id, chat_session_id)

    logger.info(f"Found : {len(chat_events)} chat events")

    return chat_events
