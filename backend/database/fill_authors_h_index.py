import logging
from datetime import datetime

from pymongo import UpdateOne

from operations import Operations

logging.basicConfig(level=logging.NOTSET)
database_fill_h_index_logger = logging.getLogger('database_fill_h_index')
database_fill_h_index_logger.setLevel(level=logging.DEBUG)
author_operations = Operations().author
collection = author_operations.collection
DOCUMENTS_COUNT = collection.estimated_document_count()


def main():
    init_time = datetime.now()
    current_count = 0
    chunk_size = 1000
    operations = []
    for doc in collection.find({"h_index": {"$exists": False}}, batch_size=chunk_size):
        operations.append(
            UpdateOne({"_id": doc["_id"]}, {"$set": {"h_index": author_operations.compute_h_index(doc['_id'])}})
        )
        current_count += 1
        if current_count % 100 == 0:
            current_time = datetime.now() - init_time
            progress = current_count / DOCUMENTS_COUNT
            database_fill_h_index_logger.info(f'[{current_time}] '
                                              f'progress: {progress * 100:3.2f}%, '
                                              f'documents uploaded: {current_count}, '
                                              f'speed: {current_count / current_time.total_seconds():.2f} obj/sec')
        if current_count % chunk_size == 0:
            if len(operations) > 0:
                collection.bulk_write(operations, ordered=False)
                operations = []
    if len(operations) > 0:
        collection.bulk_write(operations, ordered=False)


if __name__ == "__main__":
    main()
