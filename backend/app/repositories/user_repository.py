
from datetime import UTC

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from app.models.user import UserModel


class UserRepository:
    def __init__(self, database: AsyncDatabase):
        self.collection = database["users"]

    async def create(self, user: UserModel) -> UserModel:
        """Insert a new user into MongoDB."""

        document = user.model_dump(
            by_alias=True,
            mode="python",
        )

        result = await self.collection.insert_one(document)

        created_user = await self.collection.find_one(
            {"_id": result.inserted_id}
        )

        if created_user is None:
            raise RuntimeError("Failed to retrieve the created user.")

        return UserModel.model_validate(created_user)

    async def get_by_id(self, user_id: ObjectId) -> UserModel | None:
        """Retrieve a user using their MongoDB ObjectId."""

        document = await self.collection.find_one(
            {"_id": user_id}
        )

        if document is None:
            return None

        return UserModel.model_validate(document)

    async def get_by_github_id(self, github_id: int) -> UserModel | None:
        """Retrieve a user using their GitHub account ID."""

        document = await self.collection.find_one(
            {"github_id": github_id}
        )

        if document is None:
            return None

        return UserModel.model_validate(document)

    async def update(
        self,
        user_id: ObjectId,
        updates: dict,
    ) -> UserModel | None:
        """Update user information."""

        from datetime import datetime

        allowed_fields = {"username", "email", "avatar_url"}

        if not updates or not set(updates).issubset(allowed_fields):
            raise ValueError("Invalid or empty user update fields.")

        updates["updated_at"] = datetime.now(UTC)

        await self.collection.update_one(
            {"_id": user_id},
            {"$set": updates},
        )

        return await self.get_by_id(user_id)

    async def delete(self, user_id: ObjectId) -> bool:
        """Delete a user using their MongoDB ObjectId."""

        result = await self.collection.delete_one(
            {"_id": user_id}
        )

        return result.deleted_count == 1
