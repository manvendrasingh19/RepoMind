
from bson import ObjectId
from pymongo import ASCENDING
from pymongo.asynchronous.database import AsyncDatabase

from app.models.symbol import SymbolModel


class SymbolRepository:
    def __init__(self, database: AsyncDatabase):
        self.collection = database["symbols"]
        self.repositories = database["repositories"]
        self.files = database["indexed_files"]

    async def _verify_file_access(
        self,
        repository_id: ObjectId,
        file_id: ObjectId,
        user_id: ObjectId,
    ) -> bool:
        """Verify repository ownership and file membership."""

        repository = await self.repositories.find_one(
            {
                "_id": repository_id,
                "user_id": user_id,
            },
            {"_id": 1},
        )

        if repository is None:
            return False

        file = await self.files.find_one(
            {
                "_id": file_id,
                "repository_id": repository_id,
            },
            {"_id": 1},
        )

        return file is not None

    async def create(
        self,
        symbol: SymbolModel,
        user_id: ObjectId,
    ) -> SymbolModel:
        """Store an extracted code symbol."""

        if not await self._verify_file_access(
            symbol.repository_id,
            symbol.file_id,
            user_id,
        ):
            raise PermissionError("Repository or file access denied.")

        document = symbol.model_dump(
            by_alias=True,
            mode="python",
        )

        result = await self.collection.insert_one(document)

        created = await self.collection.find_one(
            {"_id": result.inserted_id}
        )

        if created is None:
            raise RuntimeError("Failed to retrieve the created symbol.")

        return SymbolModel.model_validate(created)

    async def get_by_id(
        self,
        symbol_id: ObjectId,
        repository_id: ObjectId,
        user_id: ObjectId,
    ) -> SymbolModel | None:
        """Retrieve a symbol from an owned repository."""

        repository = await self.repositories.find_one(
            {
                "_id": repository_id,
                "user_id": user_id,
            },
            {"_id": 1},
        )

        if repository is None:
            return None

        document = await self.collection.find_one(
            {
                "_id": symbol_id,
                "repository_id": repository_id,
            }
        )

        if document is None:
            return None

        return SymbolModel.model_validate(document)

    async def list_by_file(
        self,
        repository_id: ObjectId,
        file_id: ObjectId,
        user_id: ObjectId,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SymbolModel]:
        """List symbols extracted from a specific file."""

        if not await self._verify_file_access(
            repository_id,
            file_id,
            user_id,
        ):
            return []

        if skip < 0 or not 1 <= limit <= 500:
            raise ValueError("Invalid pagination parameters.")

        cursor = (
            self.collection.find(
                {
                    "repository_id": repository_id,
                    "file_id": file_id,
                }
            )
            .sort("start_line", ASCENDING)
            .skip(skip)
            .limit(limit)
        )

        documents = await cursor.to_list(length=limit)

        return [
            SymbolModel.model_validate(document)
            for document in documents
        ]

    async def search_by_name(
        self,
        repository_id: ObjectId,
        user_id: ObjectId,
        name: str,
        skip: int = 0,
        limit: int = 50,
    ) -> list[SymbolModel]:
        """Find symbols by exact name within a repository."""

        if skip < 0 or not 1 <= limit <= 200:
            raise ValueError("Invalid pagination parameters.")

        repository = await self.repositories.find_one(
            {
                "_id": repository_id,
                "user_id": user_id,
            },
            {"_id": 1},
        )

        if repository is None:
            return []

        cursor = (
            self.collection.find(
                {
                    "repository_id": repository_id,
                    "name": name,
                }
            )
            .sort("start_line", ASCENDING)
            .skip(skip)
            .limit(limit)
        )

        documents = await cursor.to_list(length=limit)

        return [
            SymbolModel.model_validate(document)
            for document in documents
        ]

    async def delete_by_file(
        self,
        repository_id: ObjectId,
        file_id: ObjectId,
        user_id: ObjectId,
    ) -> int:
        """Delete all symbols belonging to an owned file."""

        if not await self._verify_file_access(
            repository_id,
            file_id,
            user_id,
        ):
            return 0

        result = await self.collection.delete_many(
            {
                "repository_id": repository_id,
                "file_id": file_id,
            }
        )

        return result.deleted_count
