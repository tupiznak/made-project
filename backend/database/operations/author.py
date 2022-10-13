from typing import List, Union

import database.db_objects.author as db
from database.models.author import *
from database.connection import citations_db
# from mongoengine import QuerySet
from pymongo.database import Database
from database.operations.paper import PaperOperations


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
        return Author.parse_obj(db_author)  # else case

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

    def filter(self, author_filter: dict, exclude_author: dict = None,
               chunk_size: int = 10) -> List[Author]:
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

    def compute_h_index(self, author_id: str):
        """
        :type author_id
        :type return: int

        # Below is a GitHub description for h_index(citations: list[int])
        # We rewrited it to use the only argument author_id!
        #
        # Given an array of citations (each citation is a non-negative integer)
        # of a researcher, write a function to compute the researcher's h-index.
        #
        # According to the definition of h-index on Wikipedia:
        # "A scientist has index h if h of his/her N papers have
        # at least h citations each, and the other N − h papers have
        # no more than h citations each."
        #
        # For example, given citations = [3, 0, 6, 1, 5],
        # which means the researcher has 5 papers in total
        # and each of them had received 3, 0, 6, 1, 5 citations respectively.
        # Since the researcher has 3 papers with at least 3 citations each and
        # the remaining two with no more than 3 citations each, his h-index is 3.
        #
        # Note: If there are several possible values for h, the maximum one is taken as the h-index.
        # P.S. Taken from: https://github.com/kamyu104/LeetCode/blob/master/Python/h-index.py
        """
        db_author = self.find(author_id)  # db_object of the Class Author(Document)
        all_author_papers_ids = db_author.papers  # id's of all author's papers: list[str]
        # Create a list of all papers (of the author) citations (n_citations: int): list[ints]
        citations = [0] * len(all_author_papers_ids)  # type: List[int]
        for ind_paper, author_paper_id in enumerate(all_author_papers_ids):
            paper_n_citations = PaperOperations.get_n_citations(author_paper_id)
            if not paper_n_citations is None:
                citations[ind_paper] = paper_n_citations
        return sum(x >= i + 1 for i, x in enumerate( sorted(list(citations), reverse=True) ))


if __name__ == '__main__':
    pass
