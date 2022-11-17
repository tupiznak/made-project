import argparse
import logging

import pymongo.errors
from pymongo import UpdateMany
from pymongo.database import Database
from pprint import pprint

from connection import citations_db

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger('papers_splitter')
logger.setLevel(level=logging.DEBUG)
OBJECTS_COUNT = 5354308

COLLECTION = 'paper'
COLLECTION_TEST = 'paper_split_for_test'


def get_many_gen(database: Database, collection: str, batch_size: int, total_size: int = -1,
                 downloaded_chunk_size: int = 1000, randomize=True):
    curr_doc = 0
    batch = []
    if randomize:
        gen = database.get_collection(collection).aggregate([{"$sample": {"size": total_size}}])
    else:
        gen = database.get_collection(collection).find()
    for doc in gen.batch_size(downloaded_chunk_size):
        batch.append(doc)
        curr_doc += 1
        if curr_doc == batch_size:
            yield batch
            curr_doc = 0
            batch = []
    if len(batch) > 0:
        yield batch


def convertor(doc_list: list[dict]):
    return doc_list


def writer(database: Database, doc_list: list[dict]):
    collection = COLLECTION
    collection_test = COLLECTION_TEST
    author_col = database.get_collection('author')

    database.get_collection(collection_test).insert_many(doc_list)
    author_col.bulk_write([UpdateMany(filter={'_id': {'$in': el['authors']}},
                                      update={'$pull': {'papers': el['_id']}}) for el in doc_list
                           if el.get('authors', None) is not None])
    database.get_collection(collection).delete_many({'_id': {'$in': [el['_id'] for el in doc_list]}})


def split_collections(test_size=0.3, chunk_size=1000):
    database = citations_db
    collection = COLLECTION
    collection_test = COLLECTION_TEST
    print('before', database.get_collection(collection).estimated_document_count(),
          database.get_collection(collection_test).estimated_document_count(), )
    try:
        database.create_collection(collection_test)
    except pymongo.errors.CollectionInvalid:
        pass

    total_count = database.get_collection(collection).estimated_document_count()
    total_count = 100000
    test_count = int(total_count * test_size) - database.get_collection(collection_test).estimated_document_count()

    batch_gen = get_many_gen(database=database, collection=collection, batch_size=chunk_size, total_size=test_count,
                             downloaded_chunk_size=chunk_size)

    batches_cnt = (test_count // chunk_size + 1)
    print(batches_cnt)
    for batch_idx, doc_batch in enumerate(batch_gen):
        print(batch_idx, batches_cnt)
        if batch_idx >= batches_cnt:
            break
        writer(doc_list=convertor(doc_batch), database=database)

    print('after', database.get_collection(collection).estimated_document_count(),
          database.get_collection(collection_test).estimated_document_count(), )


def merge_collections(chunk_size=1000):
    database = citations_db
    collection = COLLECTION
    collection_test = COLLECTION_TEST
    author_col = database.get_collection('author')

    for batch_idx, doc_batch in enumerate(get_many_gen(database, collection_test, chunk_size, randomize=False)):
        author_col.bulk_write([UpdateMany(filter={'_id': {'$in': el['authors']}},
                                          update={'$addToSet': {'papers': el['_id']}}) for el in doc_batch
                               if el.get('authors', None) is not None])
        try:
            database.get_collection(collection).insert_many(doc_batch)
        except pymongo.errors.BulkWriteError:
            pass
        database.get_collection(collection_test).delete_many({'_id': {'$in': [el['_id'] for el in doc_batch]}})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='database initialisation module')
    parser.add_argument('--preprocessed-file', metavar='preprocessed_file', type=bool, default=True,
                        help='is file preprocessed? (correct.txt) [default: True]', required=False)
    parser.add_argument('--stack-size', metavar='stack_size', type=int, default=1000,
                        help='size of chunks of objects pushed to database [default: 1000]', required=False)
    parser.add_argument('--log-period', metavar='log_period', type=float, default=0.01,
                        help='period of log in percent [default: 0.01]', required=False)

    parser = parser.parse_args()

    logger.setLevel(level=logging.DEBUG)
    merge_collections()
    # split_collections()
