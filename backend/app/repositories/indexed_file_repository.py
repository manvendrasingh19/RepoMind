
from bson import ObjectId
from pymongo import ASCENDING
from pymongo.asynchronous.database import AsyncDatabase

from app.models.indexed_file import IndexedFileModel, ParsingStatus


class IndexedFileRepository:
    def __init__(self, database: AsyncDatabase):
        self.collection = database["indexed_files"]
        self.repositories = database["repositories"]

    async def _verify_ownership(
        self,
        repository_id: ObjectId,
        user_id: ObjectId,
    ) -> bool:
        """Verify that a repository belongs to the requesting user."""

        repository = await self.repositories.find_one(
            {
                "_id": repository_id,
                "user_id": user_id,
            },
            {"_id": 1},
        )

        return repository is not None

    async def create(
        self,
        indexed_file: IndexedFileModel,
        user_id: ObjectId,
    ) -> IndexedFileModel:
        """Create an indexed file after verifying repository ownership."""

        if not await self._verify_ownership(
            indexed_file.repository_id,
            user_id,
        ):
            raise PermissionError("Repository access denied.")

        document = indexed_file.model_dump(
            by_alias=True,
            mode="python",
        )

        result = await self.collection.insert_one(document)

        created = await self.collection.find_one(
            {"_id": result.inserted_id}
        )

        if created is None:
            raise RuntimeError("Failed to retrieve the indexed file.")

        return IndexedFileModel.model_validate(created)

    async def get_by_id(
        self,
        file_id: ObjectId,
        repository_id: ObjectId,
        user_id: ObjectId,
    ) -> IndexedFileModel | None:
        """Retrieve a file within an owned repository."""

        if not await self._verify_ownership(repository_id, user_id):
            return None

        document = await self.collection.find_one(
            {
                "_id": file_id,
                "repository_id": repository_id,
            }
        )

        if document is None:
            return None

        return IndexedFileModel.model_validate(document)

    async def get_by_path(
        self,
        repository_id: ObjectId,
        path: str,
        user_id: ObjectId,
    ) -> IndexedFileModel | None:
        """Find a file using its path within a repository."""

        if not await self._verify_ownership(repository_id, user_id):
            return None

        document = await self.collection.find_one(
            {
                "repository_id": repository_id,
                "path": path,
            }
        )

        if document is None:
            return None

        return IndexedFileModel.model_validate(document)

    async def list_by_repository(
        self,
        repository_id: ObjectId,
        user_id: ObjectId,
        skip: int = 0,
        limit: int = 50,
    ) -> list[IndexedFileModel]:
        """List indexed files belonging to an owned repository."""

        if not await self._verify_ownership(repository_id, user_id):
            return []

        if skip < 0 or not 1 <= limit <= 200:
            raise ValueError("Invalid pagination parameters.")

        cursor = (
            self.collection.find(
                {"repository_id": repository_id}
            )
            .sort("path", ASCENDING)
            .skip(skip)
            .limit(limit)
        )

        documents = await cursor.to_list(length=limit)

        return [
            IndexedFileModel.model_validate(document)
            for document in documents
        ]

    async def update_parsing_status(
        self,
        file_id: ObjectId,
        repository_id: ObjectId,
        user_id: ObjectId,
        status: ParsingStatus,
    ) -> IndexedFileModel | None:
        """Update the parsing status of an indexed file."""

        if not await self._verify_ownership(repository_id, user_id):
            return None

        await self.collection.update_one(
            {
                "_id": file_id,
                "repository_id": repository_id,
            },
            {
                "$set": {
                    "parsing_status": status,
                }
            },
        )

        return await self.get_by_id(
            file_id,
            repository_id,
            user_id,
        )

    async def delete(
        self,
        file_id: ObjectId,
        repository_id: ObjectId,
        user_id: ObjectId,
    ) -> bool:
        """Delete a file from an owned repository."""

        if not await self._verify_ownership(repository_id, user_id):
            return False

        result = await self.collection.delete_one(
            {
                "_id": file_id,
                "repository_id": repository_id,
            }
        )

        return result.deleted_count == 1
