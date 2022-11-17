import argparse
import logging
from datetime import datetime, timedelta

import pymongo.errors
from pymongo import UpdateMany
from pymongo.database import Database

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
    collection_test = COLLECTION_TEST
    author_col = database.get_collection('author')

    database.get_collection(collection_test).insert_many(doc_list)
    author_col.bulk_write([UpdateMany(filter={'_id': {'$in': el['authors']}},
                                      update={'$pull': {'papers': el['_id']}}) for el in doc_list
                           if el.get('authors', None) is not None])


def split_collections(test_size=0.3, chunk_size=1000):
    database = citations_db
    collection = COLLECTION
    collection_test = COLLECTION_TEST
    total_count = database.get_collection(collection).estimated_document_count()
    total_count_test = database.get_collection(collection_test).estimated_document_count()
    database[collection_test].create_index('authors')
    logger.info(f'start splitting... before sizes: train = {total_count}, test = {total_count_test}')
    try:
        database.create_collection(collection_test)
    except pymongo.errors.CollectionInvalid:
        pass

    # total_count = 100000
    test_count = int(total_count * test_size) - database.get_collection(collection_test).estimated_document_count()
    if test_count <= 0:
        logger.info(f'delta {test_count=}')
        return

    exist_papers = set()
    while True:
        doc_batch = list(database.get_collection(collection).aggregate([
            {"$sample": {"size": chunk_size}}
        ]))
        doc_batch = [d for d in doc_batch if d['_id'] not in exist_papers]
        if len(doc_batch) == 0:
            logger.warning(f'batch size empty after filter')
            continue
        writer(doc_list=convertor(doc_batch), database=database)
        exist_papers |= set(d['_id'] for d in doc_batch)
        logger.debug(f'split {len(exist_papers) / test_count * 100:.2f}% curr test papers {len(exist_papers)}')
        if len(exist_papers) >= test_count:
            break

    logger.info(f'remove papers from train')
    exist_papers = list(exist_papers)
    for part in range(len(exist_papers) // chunk_size + 1):
        database.get_collection(collection).delete_many(
            {'_id': {'$in': exist_papers[part * chunk_size:(part + 1) * chunk_size]}})

    total_count = database.get_collection(collection).estimated_document_count()
    total_count_test = database.get_collection(collection_test).estimated_document_count()
    logger.info(f'split completed. after sizes: train = {total_count}, test = {total_count_test}')


def merge_collections(batch_size=1000):
    downloaded_chunk_size = batch_size
    database = citations_db
    collection = COLLECTION
    collection_test = COLLECTION_TEST
    author_col = database.get_collection('author')
    total_count = database.get_collection(collection_test).estimated_document_count()
    database[collection_test].create_index('authors')
    logger.info(f'start merging... {total_count}')

    for batch_idx, doc_batch in enumerate(get_many_gen(
            database, collection_test,
            batch_size=batch_size, downloaded_chunk_size=downloaded_chunk_size, randomize=False)):
        author_col.bulk_write([UpdateMany(filter={'_id': {'$in': el['authors']}},
                                          update={'$addToSet': {'papers': el['_id']}}) for el in doc_batch
                               if el.get('authors', None) is not None])
        try:
            database.get_collection(collection).insert_many(doc_batch)
        except pymongo.errors.BulkWriteError:
            pass
        database.get_collection(collection_test).delete_many({'_id': {'$in': [el['_id'] for el in doc_batch]}})
        logger.debug(f'merged {batch_idx * batch_size / total_count * 100:.2f}%')

    logger.info('merge completed')


class DeltaTimeFormatter(logging.Formatter):
    def format(self, record):
        duration = datetime.utcfromtimestamp(record.relativeCreated / 1000)
        record.delta = duration.strftime("%H:%M:%S")
        return super().format(record)


class DeltaTimeHandler(logging.StreamHandler):
    def __init__(self):
        self.prev_time = datetime.now()
        super().__init__()

    def emit(self, record) -> None:
        if record.levelname != 'DEBUG':
            self.prev_time = datetime.now()
            return super().emit(record)
        if datetime.now() > self.prev_time + timedelta(seconds=5):
            self.prev_time = datetime.now()
            return super().emit(record)


if __name__ == '__main__':
    col_new = citations_db[COLLECTION_TEST]
    col_old = citations_db[COLLECTION]
    for el in col_new.find():
        col_old.delete_one({'_id': el['_id']})
    exit()

    parser = argparse.ArgumentParser(description='database initialisation module')
    parser.add_argument('--preprocessed-file', metavar='preprocessed_file', type=bool, default=True,
                        help='is file preprocessed? (correct.txt) [default: True]', required=False)
    parser.add_argument('--stack-size', metavar='stack_size', type=int, default=1000,
                        help='size of chunks of objects pushed to database [default: 1000]', required=False)
    parser.add_argument('--log-period', metavar='log_period', type=float, default=0.01,
                        help='period of log in percent [default: 0.01]', required=False)

    parser = parser.parse_args()

    logger.setLevel(level=logging.DEBUG)

    handler = DeltaTimeHandler()
    formatter = DeltaTimeFormatter("+%(delta)s - %(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    # merge_collections()
    split_collections()
