
from datetime import UTC, datetime
from enum import StrEnum

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from app.models.common import PyObjectId


class SymbolKind(StrEnum):
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    VARIABLE = "variable"
    CONSTANT = "constant"
    INTERFACE = "interface"
    ENUM = "enum"
    PROPERTY = "property"


class SymbolModel(BaseModel):
    id: PyObjectId = Field(
        default_factory=ObjectId,
        alias="_id",
    )

    repository_id: PyObjectId
    file_id: PyObjectId

    name: str
    qualified_name: str
    kind: SymbolKind

    signature: str | None = None
    docstring: str | None = None

    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )
