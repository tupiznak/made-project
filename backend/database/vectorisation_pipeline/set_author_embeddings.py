import logging
from datetime import datetime

import click
import fasttext
from pymongo import UpdateMany
from pymongo.database import Database

from database.connection import citations_db
from enities.title_params import read_vectorizing_pipeline_params

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


def writer(database: Database, doc_list: list[dict], model: fasttext.FastText):
    # collection_test = COLLECTION_TEST
    author_col = database.get_collection('author')

    # database.get_collection(collection_test).insert_many(doc_list)
    # print(doc_list)
    author_col.bulk_write([UpdateMany(
        filter={'_id': {'$in': el['authors']}},
        update={'$set': {
            f'vectorized_papers.{el["_id"]}': model.get_word_vector(el["title"]).tolist()}})
        for el in doc_list if el.get('authors', None) is not None])


@click.command("set_author_embedding")
@click.argument("config_path")
def set_author_embedding(config_path: str):
    params = read_vectorizing_pipeline_params(
        config_path).author_embeddings_params
    batch_size = params.batch_size
    database = citations_db
    # author_operations = Operations().author
    collection = "paper"  # author_operations.collection
    model = fasttext.load_model("models/fasttext_vectorizer.bin")

    init_time = datetime.now()
    for batch_cnt, papers in enumerate(get_many_gen(database, collection, batch_size)):
        writer(database, papers, model)
        current_time = datetime.now() - init_time
        current_count = batch_cnt * batch_size
        progress = current_count / OBJECTS_COUNT
        database_changer_logger.info(f'[{current_time}] '
                                     f'progress: {progress * 100:3.2f}%, '
                                     f'documents uploaded: {current_count}, '
                                     f'speed: {current_count / current_time.total_seconds():.2f} obj/sec')


if __name__ == '__main__':
    set_author_embedding()
