from typing import List, Union

import database.db_objects.author as db
from database.models.author import *
from database.connection import citations_db
# from mongoengine import QuerySet
from pymongo.database import Database

from datetime import datetime


class AuthorOperations:

    def __init__(self, database: Database = citations_db):
        self.db = database

    @property
    def collection(self):
        return self.db['author']

    def flush(self):
        self.db.drop_collection('author')

    def to_model(self, db_author: Union[db.Author, dict]) -> Author:
        if isinstance(db_author, db.Author):
            return Author.parse_raw(db_author.to_json())
        else:
            return Author.parse_obj(db_author)

    def replace_id(self, author: dict):
        author['_id'] = author['id']
        del author['id']
        return author

    def model_to_db(self, author: Author) -> db.Author:
        return db.Author(**author.dict(by_alias=True))

    def create(self, author: Author) -> Author:
        db_author = self.model_to_db(author)
        db_author.save(force_insert=True)
        return author

    def find(self, _id: str) -> db.Author:
        return db.Author.objects.get(_id=_id)

    def get_by_id(self, _id: str) -> Author:
        db_author = self.find(_id)
        author = self.to_model(db_author)
        return author

    def full_update(self, author: Author) -> Author:
        db_author = self.model_to_db(author)
        db_author.save()
        return self.to_model(db_author)

    def change_name(self, _id: str, name: str) -> Author:
        db_author = self.find(_id)
        db_author.name = name
        db_author.save()
        return self.to_model(db_author)

    def get_chunk(self, id_list: List[str] = None, chunk_size: int = 10) -> List[Author]:
        if id_list is None:
            cmd = db.Author.objects.aggregate([{'$sample': {'size': chunk_size}}])
            db_authors = [c for c in cmd]
            authors = [self.to_model(p) for p in db_authors]
        else:
            authors = []
            for i in id_list:
                authors.append(self.get_by_id(i))
        return authors

    def delete(self, _id: str):
        author = self.get_by_id(_id)
        self.collection.delete_one(dict(_id=author.id))

    def filter(self, author_filter: dict, exclude_author: dict = None, chunk_size: int = 10) -> List[Author]:
        if exclude_author is None:
            exclude_author = {}
        exclude_author = dict((f'{k}__ne', v) for k, v in exclude_author.items())
        cmd = db.Author.objects.filter(**(author_filter | exclude_author)) \
            .aggregate([{'$sample': {'size': chunk_size}}])
        db_objects = [c for c in cmd]
        authors = [self.to_model(p) for p in db_objects]
        return authors

    def total_size(self):
        return self.collection.estimated_document_count()

    def get_authors_by_org(self, org_id: str, chunk_size: int = 10) -> List[Author]:
        query = self.collection.aggregate([
            {
                '$match': {
                    'org': org_id
                }
            },
            {
                '$sample': {
                    'size': chunk_size
                }
            }
        ])
        db_objects = [o for o in query]
        authors = [self.to_model(p) for p in db_objects]
        return authors

    def like(self, paper_id: str, _id: str):
        db_author = self.find(_id)
        db_author.history.append(db.HistoryObject(
            event=paper_id, event_time=datetime.now(),
            event_description=f'like at paper {paper_id}'))
        db_author.save()
        return db_author

    def get_history(self, _id: str) -> List:
        db_author = self.find(_id)
        return [event.to_mongo() for event in db_author.history]


if __name__ == '__main__':
    pass
