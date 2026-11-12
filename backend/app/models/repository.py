
from datetime import UTC, datetime
from enum import StrEnum

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from app.models.common import PyObjectId


class IndexingStatus(StrEnum):
    PENDING = "pending"
    QUEUED = "queued"
    INDEXING = "indexing"
    COMPLETED = "completed"
    FAILED = "failed"


class RepositoryModel(BaseModel):
    id: PyObjectId = Field(
        default_factory=ObjectId,
        alias="_id",
    )

    user_id: PyObjectId

    github_repo_id: int
    full_name: str
    description: str | None = None

    owner: str
    name: str
    default_branch: str = "main"

    is_private: bool = False
    html_url: str

    indexed_commit_sha: str | None = None
    indexing_status: IndexingStatus = IndexingStatus.PENDING

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )
