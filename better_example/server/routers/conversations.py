from typing import Annotated
from logger.custom_logger import logger

from db import models
from db.crud_conversation import create_conversation, get_conversations
from db.database import get_db
from fastapi import APIRouter, Depends, Request
from logger.custom_logger import logger_bind
from server.auth import RoleChecker, get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

allow_create_user = RoleChecker(["admin"])
allow_delete_user = RoleChecker(["admin"])


# Init new conversation
@router.post("/conversations")
async def post_conversation(
    user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    # Generate new conversation
    conversation = create_conversation(db, user.id)

    logger = logger_bind(conversation.id, None)
    logger.info(
        "Username: {} started new conversation with ID {}",
        user.username,
        conversation.id,
    )

    return conversation


@router.get("/conversations")
async def read_conversations(
    request: Request,
    user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    type = request.query_params.get("type")

    # Get conversation of type "NEW", which are the headers of the conversations
    conversations = get_conversations(db, user.id, None, type)

    logger.info(f"Found : {len(conversations)} conversations")

    return conversations


@router.get("/conversations/{conversation_id}")
async def get_conversations(
    request: Request,
    user: Annotated[models.User, Depends(get_current_user)],
    conversation_id: str,
    db: Session = Depends(get_db),
):
    type = request.query_params.get("type")

    conversations = get_conversations(db, user.id, conversation_id, type)

    logger.info(f"Found : {len(conversations)} conversations")

    return conversations
