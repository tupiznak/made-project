import logging
from datetime import datetime

from operations import Operations

logging.basicConfig(level=logging.NOTSET)
database_fill_h_index_logger = logging.getLogger('database_fill_h_index')
database_fill_h_index_logger.setLevel(level=logging.DEBUG)
author_operations = Operations().author
collection = author_operations.collection
DOCUMENTS_COUNT = collection.estimated_document_count()


def main():
    pass


if __name__ == "__main__":
    init_time = datetime.now()
    current_count = 0
    chunk_size = 10
    batch_h_indexes = [0]*chunk_size
    batch_author_ids = [0]*chunk_size
    for doc in collection.find({"h_index": {"$exists": False}}, batch_size = chunk_size):
        print(doc)
        author_operations.set_h_index(doc['_id'])
        current_count += 1
        if current_count % chunk_size == 0:
            current_time = datetime.now() - init_time
            progress = current_count / DOCUMENTS_COUNT
            database_fill_h_index_logger.info(f'[{current_time}] '
                                              f'progress: {progress * 100:3.2f}%, '
                                              f'documents uploaded: {current_count}, '
                                              f'speed: {current_count / current_time.total_seconds():.2f} obj/sec')

