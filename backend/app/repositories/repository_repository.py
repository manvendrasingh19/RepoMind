
from datetime import UTC, datetime

from bson import ObjectId
from pymongo import DESCENDING
from pymongo.asynchronous.database import AsyncDatabase

from app.models.repository import IndexingStatus, RepositoryModel


class RepositoryRepository:
    def __init__(self, database: AsyncDatabase):
        self.collection = database["repositories"]

    async def create(
        self,
        repository: RepositoryModel,
    ) -> RepositoryModel:
        """Create a repository for a user."""

        document = repository.model_dump(
            by_alias=True,
            mode="python",
        )

        result = await self.collection.insert_one(document)

        created = await self.collection.find_one(
            {"_id": result.inserted_id}
        )

        if created is None:
            raise RuntimeError("Failed to retrieve the created repository.")

        return RepositoryModel.model_validate(created)

    async def get_by_id(
        self,
        repository_id: ObjectId,
        user_id: ObjectId,
    ) -> RepositoryModel | None:
        """Retrieve a repository belonging to a specific user."""

        document = await self.collection.find_one(
            {
                "_id": repository_id,
                "user_id": user_id,
            }
        )

        if document is None:
            return None

        return RepositoryModel.model_validate(document)

    async def get_by_github_repo_id(
        self,
        github_repo_id: int,
        user_id: ObjectId,
    ) -> RepositoryModel | None:
        """Find a user's repository using its GitHub ID."""

        document = await self.collection.find_one(
            {
                "github_repo_id": github_repo_id,
                "user_id": user_id,
            }
        )

        if document is None:
            return None

        return RepositoryModel.model_validate(document)

    async def list_by_user(
        self,
        user_id: ObjectId,
        skip: int = 0,
        limit: int = 20,
    ) -> list[RepositoryModel]:
        """List repositories belonging to a user."""

        if skip < 0 or not 1 <= limit <= 100:
            raise ValueError("Invalid pagination parameters.")

        cursor = (
            self.collection.find({"user_id": user_id})
            .sort("updated_at", DESCENDING)
            .skip(skip)
            .limit(limit)
        )

        documents = await cursor.to_list(length=limit)

        return [
            RepositoryModel.model_validate(document)
            for document in documents
        ]

    async def update_indexing_status(
        self,
        repository_id: ObjectId,
        user_id: ObjectId,
        status: IndexingStatus,
        indexed_commit_sha: str | None = None,
    ) -> RepositoryModel | None:
        """Update indexing status for a user's repository."""

        updates = {
            "indexing_status": status,
            "updated_at": datetime.now(UTC),
        }

        if indexed_commit_sha is not None:
            updates["indexed_commit_sha"] = indexed_commit_sha

        await self.collection.update_one(
            {
                "_id": repository_id,
                "user_id": user_id,
            },
            {"$set": updates},
        )

        return await self.get_by_id(repository_id, user_id)

    async def delete(
        self,
        repository_id: ObjectId,
        user_id: ObjectId,
    ) -> bool:
        """Delete a repository belonging to a specific user."""

        result = await self.collection.delete_one(
            {
                "_id": repository_id,
                "user_id": user_id,
            }
        )

        return result.deleted_count == 1
