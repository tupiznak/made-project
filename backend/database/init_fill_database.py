import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple

import pymongo.errors
from pymongo import MongoClient

from .connection import citations_db, new_connection
from .load_json import parse_json, json_parser_logger

logging.basicConfig(level=logging.NOTSET)
database_init_logger = logging.getLogger('database_init')
database_init_logger.setLevel(level=logging.DEBUG)


def write_data(pair: Tuple[MongoClient, dict]):
    db_client, data = pair
    try:
        citations_db['paper'].insert_one(data)
    except pymongo.errors.DuplicateKeyError as e:
        database_init_logger.debug(f'id duplicated: {e}')


def init_database(json_path: str, flush: bool = False, parallel_db_writers: int = 100):
    if flush:
        citations_db.drop_collection('paper')
    connections: Tuple[MongoClient] = tuple(new_connection() for _ in range(parallel_db_writers))
    parsed_stack = []
    for doc in parse_json(file_path=json_path):
        parsed_stack.append(doc)
        if len(parsed_stack) > 0 and len(parsed_stack) % (parallel_db_writers) == 0:
            with ThreadPoolExecutor(max_workers=parallel_db_writers) as conn_pool_executor:
                send_data = list(zip(connections, parsed_stack))
                conn_pool_executor.map(write_data, send_data)
                parsed_stack = []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='database initialisation module')
    parser.add_argument('--file-path', metavar='file_path', type=str,
                        help='json file location', required=True)
    parser.add_argument('--flush', metavar='flush', type=bool, default=False,
                        help='flush database before initialization [default: False]', required=False)

    parser = parser.parse_args()

    database_init_logger.setLevel(level=logging.DEBUG)
    json_parser_logger.setLevel(level=logging.ERROR)
    init_database(flush=parser.flush, json_path=parser.file_path)
