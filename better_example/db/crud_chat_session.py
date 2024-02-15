from collections import defaultdict
from typing import DefaultDict, List

from db import schemas
from server.id import generate_id
from sqlalchemy.orm import Session

from . import models


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
) -> List[schemas.ChatEventBase]:
    throw_if_chat_session_not_found(db, user_id, chat_session_id)

    # The chat_events variable contains a stream of all events for the given chat_session_id
    chat_events = (
        db.query(models.ChatEvent)
        .filter(models.ChatEvent.chat_session_id == chat_session_id)
        .order_by(models.ChatEvent.created_at)
        .all()
    )

    # Reduce the (low level) list of all chat_events to a list of nicer shaped ChatEventBase instances grouped by query_id

    # Order chat events by query_id
    chat_events_by_query_id: DefaultDict[str, List[models.ChatEvent]] = defaultdict(
        list[models.ChatEvent]
    )
    for chat_event in chat_events:
        chat_events_by_query_id[chat_event.query_id].append(chat_event)

    # Create a list of ChatEventBase instances
    result: List[schemas.ChatEventBase] = []

    for query_id, chat_events in chat_events_by_query_id.items():
        # Create a ChatEventBase instance
        result_item = schemas.ChatEventBase(query_id=query_id)

        # Populate the query and answer fields
        query_request = next(
            (x for x in chat_events if x.type == "QUERY_REQUEST"), None
        )
        result_item.query = query_request.content if query_request else None

        answer = next((x for x in chat_events if x.type == "QUERY_RESPONSE"), None)
        result_item.answer = answer.content if answer else None

        # Populate the feedback field
        result_item.feedback = schemas.ChatFeedbackBase(sentiment="none", items=[])

        feedbacks = filter(lambda x: x.type == "Feedback", chat_events)
        if feedbacks:
            for feedback in feedbacks:
                result_item.feedback.items.append(
                    schemas.FeedbackItem(
                        text=feedback.content, date=feedback.created_at
                    )
                )

        sentiments = list(filter(lambda x: x.type == "Sentiment", chat_events))
        result_item.feedback.sentiment = (
            sentiments[-1].content if sentiments else "none"
        )

        result.append(result_item)

    return result


def throw_if_chat_session_not_found(db: Session, user_id: int, chat_session_id: str):
    # get_chat_session will return None if chat session is not found
    # This includes a check if the chat session belongs to the user
    chat_session = get_chat_session(db, user_id, chat_session_id)
    if not chat_session:
        raise ValueError(f"Chat session {chat_session_id} not found")
