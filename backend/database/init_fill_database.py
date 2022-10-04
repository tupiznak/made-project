import argparse
import json
import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pymongo.errors
from pymongo import UpdateOne
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
    authors_by_paper: dict[str, list[dict]] = defaultdict(list)
    author_by_author_id: dict[str, dict] = {}
    papers_by_author_id: dict[str, list[str]] = defaultdict(list)
    papers = []
    for d in data:
        # parse venues
        if d.get('venue', None) is not None:
            if d['venue'].get('_id', None) is not None:
                d['venue']['papers_count'] = 1
                venues[d['_id']] = d['venue']
                d['venue'] = d['venue']['_id']

        # parse authors
        if d.get('authors', None) is not None:
            for author in d['authors']:
                if author.get('_id', None) is not None:
                    authors_by_paper[d['_id']].append(author)
                    author_by_author_id[author['_id']] = author
                    papers_by_author_id[author['_id']].append(d['_id'])
            d['authors'] = [author['_id'] for author in authors_by_paper[d['_id']]]

        paper = d
        papers.append(paper)

    # insert papers
    # FIXME not work with flush=False
    try:
        db['paper'].insert_many(papers, ordered=False)
    except pymongo.errors.PyMongoError as e:
        for paper in papers:
            if paper['_id'] in str(e):
                del venues[paper['_id']]

    # insert venues
    venues_id = [v['_id'] for v in venues.values()]
    db['venue'].update_many(filter={'_id': {'$in': venues_id}},
                            update={'$inc': {'papers_count': 1}},
                            upsert=False)
    try:
        db['venue'].insert_many(venues.values(), ordered=False)
    except pymongo.errors.BulkWriteError:
        pass

    # insert authors
    author_by_author_id: list[dict] = list(author_by_author_id.values())

    author_chunks: list[list[dict]] = []
    for i in range(len(author_by_author_id) // len(data)):
        author_chunks.append(author_by_author_id[i * len(data):(i + 1) * len(data)])
    if len(author_chunks[-1]) < len(data) / 2 and len(author_chunks) > 1:
        author_chunks[-2].extend(author_chunks[-1])
        author_chunks = author_chunks[:-1]

    for chunk in author_chunks:
        try:
            db['author'].insert_many(chunk, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            pass

    db['author'].bulk_write([UpdateOne(filter={'_id': author_id},
                                       update={'$push': {'papers': {'$each': paper_ids}}})
                             for author_id, paper_ids in papers_by_author_id.items()])


def init_database(json_path: str, flush: bool = False,
                  stack_size: int = 1000, parallel_db_writers: int = 2):
    if flush:
        client.drop_database(citations_db.name)
    citations_db['paper'].create_index('venue')
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
                       stack_size: int = 1000, parallel_db_writers: int = 2,
                       log_period_percent: float = 0.01):
    if flush:
        client.drop_database(citations_db.name)
    citations_db['paper'].create_index('venue')
    connections: tuple[Database] = tuple(new_connection()[1] for _ in range(parallel_db_writers))
    parsed_stack = []
    curr_objects_count = 0
    init_time = datetime.now()
    previous_progress = 0
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
                if progress - previous_progress > log_period_percent:
                    previous_progress = progress
                    full_time = datetime.now() - init_time
                    database_init_logger.debug(f'[{full_time}] '
                                               f'progress: {progress * 100:3.2f}%, '
                                               f'documents uploaded: {curr_objects_count}, '
                                               f'speed: {curr_objects_count / full_time.total_seconds():.0f} obj/sec')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='database initialisation module')
    parser.add_argument('--file-path', metavar='file_path', type=str,
                        help='json file location', required=True)
    parser.add_argument('--flush', metavar='flush', type=bool, default=True,
                        help='flush database before initialization [default: True]', required=False)
    parser.add_argument('--preprocessed-file', metavar='preprocessed_file', type=bool, default=True,
                        help='is file preprocessed? (correct.txt) [default: True]', required=False)
    parser.add_argument('--stack-size', metavar='stack_size', type=int, default=1000,
                        help='size of chunks of objects pushed to database [default: 1000]', required=False)
    parser.add_argument('--log-period', metavar='log_period', type=float, default=0.01,
                        help='period of log in percent [default: 0.01]', required=False)

    parser = parser.parse_args()
    if parser.flush:
        database_init_logger.warning('database will bi flashed!!! Sure?')
        # input()

    database_init_logger.setLevel(level=logging.DEBUG)
    json_parser_logger.setLevel(level=logging.ERROR)
    if parser.preprocessed_file:
        init_database_fast(flush=parser.flush, jsonl_path=parser.file_path,
                           stack_size=parser.stack_size, log_period_percent=parser.log_period)
    else:
        init_database(flush=parser.flush, json_path=parser.file_path, stack_size=parser.stack_size)
