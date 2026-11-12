
from pymongo import ASCENDING, DESCENDING, IndexModel
from pymongo.asynchronous.database import AsyncDatabase


async def initialize_indexes(database: AsyncDatabase) -> None:
    """Create indexes for all RepoMind MongoDB collections."""

    index_definitions = {
        "users": [
            IndexModel(
                [("github_id", ASCENDING)],
                unique=True,
                name="idx_users_github_id_unique",
            ),
        ],

        "repositories": [
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("github_repo_id", ASCENDING),
                ],
                unique=True,
                name="idx_repositories_user_github_repo_unique",
            ),
            IndexModel(
                [("user_id", ASCENDING), ("updated_at", DESCENDING)],
                name="idx_repositories_user_updated",
            ),
        ],

        "indexed_files": [
            IndexModel(
                [("repository_id", ASCENDING), ("path", ASCENDING)],
                unique=True,
                name="idx_files_repository_path_unique",
            ),
            IndexModel(
                [("repository_id", ASCENDING), ("blob_sha", ASCENDING)],
                name="idx_files_repository_blob",
            ),
        ],

        "symbols": [
            IndexModel(
                [
                    ("repository_id", ASCENDING),
                    ("file_id", ASCENDING),
                    ("qualified_name", ASCENDING),
                    ("start_line", ASCENDING),
                ],
                name="idx_symbols_repository_file_name_line",
            ),
            IndexModel(
                [("repository_id", ASCENDING), ("name", ASCENDING)],
                name="idx_symbols_repository_name",
            ),
        ],

        "dependencies": [
            IndexModel(
                [
                    ("repository_id", ASCENDING),
                    ("source_symbol_id", ASCENDING),
                    ("target_symbol_id", ASCENDING),
                    ("relation", ASCENDING),
                ],
                unique=True,
                name="idx_dependencies_relationship_unique",
            ),
            IndexModel(
                [("repository_id", ASCENDING), ("source_symbol_id", ASCENDING)],
                name="idx_dependencies_source",
            ),
            IndexModel(
                [("repository_id", ASCENDING), ("target_symbol_id", ASCENDING)],
                name="idx_dependencies_target",
            ),
        ],

        "conversations": [
            IndexModel(
                [("user_id", ASCENDING), ("updated_at", DESCENDING)],
                name="idx_conversations_user_updated",
            ),
        ],

        "messages": [
            IndexModel(
                [("conversation_id", ASCENDING), ("created_at", ASCENDING)],
                name="idx_messages_conversation_created",
            ),
        ],

        "indexing_jobs": [
            IndexModel(
                [("repository_id", ASCENDING), ("created_at", DESCENDING)],
                name="idx_jobs_repository_created",
            ),
            IndexModel(
                [("status", ASCENDING), ("created_at", ASCENDING)],
                name="idx_jobs_status_created",
            ),
        ],
    }

    for collection_name, indexes in index_definitions.items():
        await database[collection_name].create_indexes(indexes)
        print(f"Indexes initialized: {collection_name}")

    print("All RepoMind MongoDB indexes initialized.")
