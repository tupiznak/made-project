import argparse
import json
import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pymongo.errors
from pymongo.database import Database

from .connection import citations_db, client, new_connection
from .load_json import parse_json, json_parser_logger

logging.basicConfig(level=logging.NOTSET)
database_init_logger = logging.getLogger('database_init')
database_init_logger.setLevel(level=logging.DEBUG)
OBJECTS_COUNT = 5354308


def write_data(pair: tuple[Database, dict]):
    db, data = pair
    venues: dict[str, dict] = {}
    authors: dict[str, list[dict]] = defaultdict(list)
    papers = []
    for d in data:
        if d.get('venue', None) is not None:
            if d['venue'].get('_id', None) is not None:
                d['venue']['papers_count'] = 1
                venues[d['_id']] = d['venue']
                d['venue'] = d['venue']['_id']
        if d.get('authors', None) is not None:
            for author in d['authors']:
                if author.get('_id', None) is not None:
                    author['papers_count'] = 1
                    authors[d['_id']].append(author)
            d['authors'] = [author['_id'] for author in authors[d['_id']]]
        paper = d
        papers.append(paper)
    try:
        db['paper'].insert_many(papers, ordered=False)
    except pymongo.errors.PyMongoError as e:
        for paper in papers:
            if paper['_id'] in str(e):
                del venues[paper['_id']]
    try:
        venues_id = [v['_id'] for v in venues.values()]
        db['venue'].update_many(filter={'_id': {'$in': venues_id}},
                                update={'$inc': {'papers_count': 1}},
                                upsert=False)
    except pymongo.errors.PyMongoError as e:
        database_init_logger.debug(f'id venue duplicated: {e}')
    try:
        db['venue'].insert_many(venues.values(), ordered=False)
    except pymongo.errors.BulkWriteError:
        pass


def init_database(json_path: str, flush: bool = False, stack_size: int = 1000, parallel_db_writers: int = 2):
    if flush:
        client.drop_database(citations_db.name)
    connections: tuple[Database] = tuple(new_connection()[1] for _ in range(parallel_db_writers))
    parsed_stack = []
    for doc in parse_json(file_path=json_path):
        parsed_stack.append(doc)
        if len(parsed_stack) > 0 and len(parsed_stack) % (stack_size * parallel_db_writers) == 0:
            with ThreadPoolExecutor(max_workers=parallel_db_writers) as conn_pool_executor:
                parsed_stack = tuple(parsed_stack[i * stack_size:(i + 1) * stack_size]
                                     for i in range(parallel_db_writers))
                send_data = list(zip(connections, parsed_stack))
                conn_pool_executor.map(write_data, send_data)
                parsed_stack = []


def init_database_fast(jsonl_path: str, flush: bool = False,
                       stack_size: int = 1000, parallel_db_writers: int = 2):
    if flush:
        client.drop_database(citations_db.name)
    connections: tuple[Database] = tuple(new_connection()[1] for _ in range(parallel_db_writers))
    parsed_stack = []
    curr_objects_count = 0
    init_time = datetime.now()
    with open(jsonl_path) as f:
        for doc in f:
            parsed_stack.append(json.loads(doc))
            if len(parsed_stack) > 0 and len(parsed_stack) % (stack_size * parallel_db_writers) == 0:
                with ThreadPoolExecutor(max_workers=parallel_db_writers) as conn_pool_executor:
                    parsed_stack = tuple(parsed_stack[i * stack_size:(i + 1) * stack_size]
                                         for i in range(parallel_db_writers))
                    send_data = list(zip(connections, parsed_stack))
                    conn_pool_executor.map(write_data, send_data)
                    parsed_stack = []
                curr_objects_count += stack_size * parallel_db_writers
                progress = curr_objects_count / OBJECTS_COUNT
                database_init_logger.debug(f'[{datetime.now() - init_time}] '
                                           f'progress: {progress * 100:3.2f}%, '
                                           f'documents uploaded: {curr_objects_count}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='database initialisation module')
    parser.add_argument('--file-path', metavar='file_path', type=str,
                        help='json file location', required=True)
    parser.add_argument('--flush', metavar='flush', type=bool, default=True,
                        help='flush database before initialization [default: True]', required=False)
    parser.add_argument('--preprocessed-file', metavar='preprocessed_file', type=bool, default=True,
                        help='is file preprocessed? (correct.txt) [default: True]', required=False)

    parser = parser.parse_args()
    if parser.flush:
        database_init_logger.warning('database will bi flashed!!! Sure?')
        # input()

    database_init_logger.setLevel(level=logging.DEBUG)
    json_parser_logger.setLevel(level=logging.ERROR)
    if parser.preprocessed_file:
        init_database_fast(flush=parser.flush, jsonl_path=parser.file_path)
    else:
        init_database(flush=parser.flush, json_path=parser.file_path)
