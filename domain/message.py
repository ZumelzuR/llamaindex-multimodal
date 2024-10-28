from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import List


class Role(str, Enum):
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    role: Role
    message: str
    date: datetime = None


class MessageRequest(BaseModel):
    history: List[Message] = []
    message: str
