import logging
from datetime import datetime

import click
import fasttext
from pymongo import UpdateMany
from pymongo.database import Database

from database.connection import citations_db
from database.split_train_test import DeltaTimeHandler, DeltaTimeFormatter

# logging.basicConfig(level=logging.NOTSET)
# database_changer_logger = logging.getLogger('database_changer')
# database_changer_logger.setLevel(level=logging.DEBUG)
OBJECTS_COUNT = 5354308

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger('database_changer')
logger.setLevel(level=logging.DEBUG)


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


def writer(database: Database, doc_list: list[dict], model: fasttext.FastText):
    author_col = database.get_collection('author')

    # print(doc_list)
    author_col.bulk_write([UpdateMany(
        filter={'_id': {'$in': el['authors']}},
        update={'$set': {
            f'vectorized_papers.{el["_id"]}': model.get_word_vector(el["title"]).tolist()}})
        for el in doc_list if el.get('authors', None) is not None and el.get('title', None) is not None])


@click.command("set_author_embedding")
@click.argument("config_path")
def set_author_embedding(config_path: str):
    batch_size = 1000
    database = citations_db
    collection = "paper"  # author_operations.collection
    model = fasttext.load_model("models/fasttext_vectorizer.bin")

    init_time = datetime.now()
    for batch_cnt, papers in enumerate(get_many_gen(database, collection, batch_size)):
        writer(database, papers, model)
        current_time = datetime.now() - init_time
        current_count = batch_cnt * batch_size
        progress = current_count / OBJECTS_COUNT
        logger.debug(f'progress: {progress * 100:3.2f}%, '
                     f'documents uploaded: {current_count}, '
                     f'speed: {current_count / current_time.total_seconds():.2f} obj/sec')


if __name__ == '__main__':
    logger.setLevel(level=logging.DEBUG)

    handler = DeltaTimeHandler()
    formatter = DeltaTimeFormatter("+%(delta)s - %(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    set_author_embedding()
