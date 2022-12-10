from fastapi import APIRouter
from qdrant_client import QdrantClient

from database.operations import Operations

author_operations = Operations().author
model_router = APIRouter(prefix='/model')


@model_router.post("/predict", tags=['model'])
def model_request(_id: str, coauthors_count: int = 10) -> list[str]:
    client = QdrantClient(host="qdrant", port=6333)
    author = author_operations.get_by_id(_id)
    author_vector = [1., 2., 3., 4., 5.]

    top_coauthors = client.search(collection_name='authors', query_vector=author_vector, limit=coauthors_count)
    top_coauthors = [a.payload['id'] for a in top_coauthors]
    # top_coauthors = [author_operations.get_by_id(a) for a in top_coauthors]
    return top_coauthors
