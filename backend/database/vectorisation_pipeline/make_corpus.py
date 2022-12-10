import logging
import re
from datetime import datetime

import click

from database.operations import Operations
from enities.title_params import read_vectorizing_pipeline_params

logging.basicConfig(level=logging.NOTSET)
database_make_corpus_logger = logging.getLogger('make_corpus_logger')
database_make_corpus_logger.setLevel(level=logging.DEBUG)


@click.command("make_corpus")
@click.argument("config_path")
def make_corpus(config_path: str):
    params = read_vectorizing_pipeline_params(
        config_path).title_params
    paper_operations = Operations().paper
    collection = paper_operations.collection
    cursor = collection.find({"title": {"$regex": params.title_regex}})
    DOCUMENTS_COUNT = 5_000_000
    init_time = datetime.now()
    current_count = 0
    with open(params.corpus_path, "w") as file:
        for doc in cursor:
            title = doc["title"]
            if params.use_lowercase:
                title = str.lower(title)
            title = re.sub(f'[{params.drop_symbols}]', '', title)
            file.write(title + "\n")
            current_count += 1

            if current_count % 10000 == 0:
                current_time = datetime.now() - init_time
                progress = current_count / DOCUMENTS_COUNT
                database_make_corpus_logger.info(f'[{current_time}] '
                                                 f'progress: {progress * 100:3.2f}%, '
                                                 f'documents uploaded: {current_count}, '
                                                 f'speed: {current_count / current_time.total_seconds():.2f} obj/sec')
                if params.data_size_limit and current_count >= params.data_size_limit:
                    exit()


if __name__ == '__main__':
    make_corpus()
