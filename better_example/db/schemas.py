import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer
from typing_extensions import Literal


class UserBase(BaseModel):
    username: str
    roles: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class FeedbackItem(BaseModel):
    text: str
    date: datetime.datetime

    @field_serializer("date")
    def serialize_date(self, date: datetime.datetime):
        # Add timezone information to the date
        return date.isoformat() + "Z"


class ChatFeedbackBase(BaseModel):
    sentiment: Literal["none", "good", "bad"]
    items: list[FeedbackItem]


class ChatEventBase(BaseModel):
    query_id: str
    query: Optional[str] = None
    answer: Optional[str] = None
    error: Optional[str] = None
    sources: Optional[dict[str, list[int]]] = None
    feedback: Optional[ChatFeedbackBase] = None


class ChatSessionBase(BaseModel):
    chat_session_id: str
    name: str


class ChatSessionCreate(ChatSessionBase):
    user_id: str


class ChatSession(ChatSessionBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True
