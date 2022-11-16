import argparse
import logging
from pymongo import UpdateOne
from pymongo.database import Database
from pprint import pprint

from connection import citations_db

logging.basicConfig(level=logging.NOTSET)
database_changer_logger = logging.getLogger('database_changer')
database_changer_logger.setLevel(level=logging.DEBUG)
OBJECTS_COUNT = 5354308


def get_many_gen(database, collection: str, chunk_size: int):
    curr_doc = 0
    batch = []
    for doc in database.get_collection(collection).find().batch_size(chunk_size):
        batch.append(doc)
        curr_doc += 1
        if curr_doc == chunk_size:
            yield batch
            curr_doc = 0
            batch = []


def convertor(doc_list: list[dict]):
    return doc_list


def writer(database: Database, collection: str, doc_list: list[dict], ):
    database.get_collection(collection).bulk_write(
        [UpdateOne(filter={'_id': el['_id']}, update={'$set': el}) for el in doc_list]
    )


def change_database(chunk_size=1000):
    database = citations_db
    collection = 'author'
    print(database.get_collection(collection).estimated_document_count())
    batch_gen = get_many_gen(database=database, collection=collection, chunk_size=chunk_size)
    batches_cnt = 10
    for batch_idx, doc_batch in enumerate(batch_gen):
        if batch_idx >= batches_cnt:
            break
        writer(doc_list=convertor(doc_batch), database=database, collection=collection)

    print(database.get_collection(collection).estimated_document_count())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='database initialisation module')
    parser.add_argument('--preprocessed-file', metavar='preprocessed_file', type=bool, default=True,
                        help='is file preprocessed? (correct.txt) [default: True]', required=False)
    parser.add_argument('--stack-size', metavar='stack_size', type=int, default=1000,
                        help='size of chunks of objects pushed to database [default: 1000]', required=False)
    parser.add_argument('--log-period', metavar='log_period', type=float, default=0.01,
                        help='period of log in percent [default: 0.01]', required=False)

    parser = parser.parse_args()

    database_changer_logger.setLevel(level=logging.DEBUG)
    change_database()
