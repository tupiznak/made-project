import fasttext
import numpy as np
from fastapi import APIRouter
from qdrant_client import QdrantClient

from database.operations import Operations

author_operations = Operations().author
model_router = APIRouter(prefix='/model')

VECTOR_LENGTH = 100
model = fasttext.load_model("database/vectorisation_pipeline/models/fasttext_vectorizer.bin")


@model_router.post("/predict_by_author", tags=['model'])
def model_request(_id: str, coauthors_count: int = 10) -> list[str]:
    client = QdrantClient(host="qdrant", port=6333)
    author = author_operations.get_by_id(_id)
    author_vector = [0.0] * VECTOR_LENGTH
    if len(author.vectorized_papers) > 0:
        author_vector = np.mean(list(author.vectorized_papers.values()), axis=0, dtype=float).tolist()

    top_coauthors = client.search(collection_name='authors', query_vector=author_vector, limit=coauthors_count)
    top_coauthors = [a.payload['id'] for a in top_coauthors]
    # top_coauthors = [author_operations.get_by_id(a) for a in top_coauthors]
    return top_coauthors


@model_router.post("/predict_by_paper", tags=['model'])
def model_request(title: str, coauthors_count: int = 10) -> list[str]:
    client = QdrantClient(host="qdrant", port=6333)
    author_vector = model.get_word_vector(title).tolist()

    top_coauthors = client.search(collection_name='authors', query_vector=author_vector, limit=coauthors_count)
    top_coauthors = [a.payload['id'] for a in top_coauthors]
    # top_coauthors = [author_operations.get_by_id(a) for a in top_coauthors]
    return top_coauthors
