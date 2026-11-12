
from enum import StrEnum

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from app.models.common import PyObjectId


class DependencyType(StrEnum):
    IMPORTS = "imports"
    CALLS = "calls"
    INHERITS = "inherits"
    IMPLEMENTS = "implements"
    REFERENCES = "references"


class DependencyModel(BaseModel):
    id: PyObjectId = Field(
        default_factory=ObjectId,
        alias="_id",
    )

    repository_id: PyObjectId

    source_symbol_id: PyObjectId
    target_symbol_id: PyObjectId

    relation: DependencyType

    source_file_id: PyObjectId
    target_file_id: PyObjectId

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )
