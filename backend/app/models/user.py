
from datetime import UTC, datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.common import PyObjectId


class UserModel(BaseModel):
    id: PyObjectId = Field(
        default_factory=ObjectId,
        alias="_id",
    )

    github_id: int
    username: str
    email: EmailStr | None = None
    avatar_url: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
