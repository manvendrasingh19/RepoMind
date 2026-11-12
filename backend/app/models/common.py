
from typing import Annotated, Any

from bson import ObjectId
from pydantic import (
    BeforeValidator,
    PlainSerializer,
    WithJsonSchema,
)


def validate_object_id(value: Any) -> ObjectId:
    if isinstance(value, ObjectId):
        return value

    if isinstance(value, str) and ObjectId.is_valid(value):
        return ObjectId(value)

    raise ValueError("Invalid MongoDB ObjectId")


PyObjectId = Annotated[
    ObjectId,
    BeforeValidator(validate_object_id),
    PlainSerializer(str, return_type=str, when_used="json"),
    WithJsonSchema({"type": "string"}, mode="validation"),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]
