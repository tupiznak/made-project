import ctypes
import logging

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.http.models import PointStruct

from database.connection import citations_db
from database.fill_database_by_condition_template import get_many_gen
from database.split_train_test import DeltaTimeHandler, DeltaTimeFormatter

logging.basicConfig(level=logging.NOTSET)
logging.getLogger('httpx._client').setLevel(logging.INFO)
logger = logging.getLogger('qdrant_init')
logger.setLevel(level=logging.DEBUG)

COL_NAME = 'authors'
VECTOR_LENGTH = 100
CHUNK_SIZE = 1000


def comp_hash(s: str):
    return ctypes.c_size_t(hash(s)).value


def comp_vec(vectors: dict[str, list[float]]):
    return list(np.mean(list(vectors.values()), axis=0))


if __name__ == '__main__':
    logger.setLevel(level=logging.DEBUG)

    handler = DeltaTimeHandler()
    formatter = DeltaTimeFormatter("+%(delta)s - %(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    client = QdrantClient(host="qdrant", port=6333)
    client.recreate_collection(
        collection_name=COL_NAME,
        vectors_config=VectorParams(size=VECTOR_LENGTH, distance=Distance.COSINE),
    )
    total = citations_db.get_collection('author').estimated_document_count()
    logger.info(f'count: {total}')
    curr = 0
    for author_batch in get_many_gen(database=citations_db, collection='author', chunk_size=CHUNK_SIZE):
        curr += len(author_batch)

        # author_batch = [
        #     {'_id': '53f463c1dabfaee1c0b5dff2',
        #      'papers_vectorized': {'a1': [1., 2., 3., 4., 5.], 'a2': [4., 2., 3., 4., 5.]}},
        #     {'_id': '53f63b2edabfae597a2898a5',
        #      'papers_vectorized': {'b1': [1., 5., 3., 4., 5.], 'b2': [4., 6., 3., 4., 5.]}}
        # ]

        operation_info = client.upsert(
            collection_name=COL_NAME,
            wait=True,
            points=[PointStruct(id=comp_hash(author['_id']),
                                vector=comp_vec(author['vectorized_papers']),
                                payload={'id': author['_id']})
                    for author in author_batch if author.get('vectorized_papers', False)]
        )
        logger.debug(f'progress {curr / total * 100:.2f}%')

    # print(client.search(collection_name=COL_NAME, query_vector=[1., 2., 3., 4., 5.], limit=1)[0].payload)
    # print(client.search(collection_name=COL_NAME, query_vector=[1., 5., 3., 4., 5.], limit=1)[0].payload)
    # print(client.search(collection_name=COL_NAME, query_vector=[4., 2., 3., 4., 5.], limit=1)[0].payload)
    # print(client.search(collection_name=COL_NAME, query_vector=[4., 6., 3., 4., 5.], limit=1)[0].payload)
