
from datetime import UTC, datetime
from enum import StrEnum

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from app.models.common import PyObjectId


class ParsingStatus(StrEnum):
    PENDING = "pending"
    PARSING = "parsing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class IndexedFileModel(BaseModel):
    id: PyObjectId = Field(
        default_factory=ObjectId,
        alias="_id",
    )

    repository_id: PyObjectId

    path: str
    language: str | None = None

    blob_sha: str
    content_hash: str

    size: int = Field(ge=0)

    parsing_status: ParsingStatus = ParsingStatus.PENDING

    indexed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )
