
from datetime import UTC, datetime
from enum import StrEnum

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from app.models.common import PyObjectId


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"



class MessageCitation(BaseModel):
    file_id: PyObjectId
    file_path: str
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    symbol_id: PyObjectId | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )



class MessageModel(BaseModel):
    id: PyObjectId = Field(
        default_factory=ObjectId,
        alias="_id",
    )

    conversation_id: PyObjectId

    role: MessageRole
    content: str

    citations: list[MessageCitation] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )
