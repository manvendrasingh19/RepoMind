
# RepoMind Database Design

## 1. Overview

RepoMind uses MongoDB as its primary application database,
Qdrant as its vector database, and Redis for caching
and background-job coordination.

## 2. MongoDB Collections

### users
- _id
- github_id
- username
- email
- avatar_url
- created_at
- updated_at

### repositories
- _id
- user_id
- github_repo_id
- full_name
- description
- default_branch
- indexed_commit_sha
- indexing_status
- created_at
- updated_at

### indexed_files
- _id
- repository_id
- path
- language
- blob_sha
- content_hash
- size
- parsing_status
- indexed_at

### symbols
- _id
- repository_id
- file_id
- name
- qualified_name
- kind
- signature
- start_line
- end_line
- docstring

### dependencies
- _id
- repository_id
- source_symbol_id
- target_symbol_id
- relation
- source_file_id
- target_file_id

### conversations
- _id
- user_id
- repository_id
- title
- created_at
- updated_at

### messages
- _id
- conversation_id
- role
- content
- citations
- created_at

### indexing_jobs
- _id
- repository_id
- requested_by
- status
- progress
- error
- started_at
- completed_at

## 3. Vector Database

Qdrant stores code embeddings with payload metadata
linking each vector to its repository, file and code chunk.

## 4. Redis

Redis is used for caching, temporary state and
background-job coordination.

## 5. Database Design Principles

- Use ObjectId references for relationships.
- Add indexes to frequently queried fields.
- Enforce uniqueness for GitHub identities and repository IDs.
- Avoid storing large source files repeatedly.
- Track indexing status and commit SHA for incremental indexing.
- Keep vector embeddings separate from MongoDB records.
