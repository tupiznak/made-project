import ctypes

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.http.models import PointStruct

COL_NAME = 'authors'


def comp_hash(s: str):
    return ctypes.c_size_t(hash(s)).value


def comp_vec(vectors: dict[str, list[float]]):
    return list(np.mean(list(vectors.values()), axis=0))


if __name__ == '__main__':
    client = QdrantClient(host="qdrant", port=6333)
    client.recreate_collection(
        collection_name=COL_NAME,
        vectors_config=VectorParams(size=5, distance=Distance.COSINE),
    )
    print(client.get_collection(collection_name=COL_NAME))

    author_batch = [
        {'_id': '53f463c1dabfaee1c0b5dff2', 'papers_vectorized': {'a1': [1., 2., 3., 4., 5.], 'a2': [4., 2., 3., 4., 5.]}},
        {'_id': '53f63b2edabfae597a2898a5', 'papers_vectorized': {'b1': [1., 5., 3., 4., 5.], 'b2': [4., 6., 3., 4., 5.]}}
    ]

    operation_info = client.upsert(
        collection_name=COL_NAME,
        wait=True,
        points=[PointStruct(id=comp_hash(author['_id']),
                            vector=comp_vec(author['papers_vectorized']),
                            payload={'id': author['_id']})
                for author in author_batch]
    )

    print(client.search(collection_name=COL_NAME, query_vector=[1., 2., 3., 4., 5.], limit=1)[0].payload)
    print(client.search(collection_name=COL_NAME, query_vector=[1., 5., 3., 4., 5.], limit=1)[0].payload)
    print(client.search(collection_name=COL_NAME, query_vector=[4., 2., 3., 4., 5.], limit=1)[0].payload)
    print(client.search(collection_name=COL_NAME, query_vector=[4., 6., 3., 4., 5.], limit=1)[0].payload)
