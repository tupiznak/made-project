from functools import lru_cache
from typing import List, Union

import networkx as nx

import database.db_objects.author as db
from database.connection import citations_db
from pymongo.database import Database
from fastapi import HTTPException

from database.models.author import Author, HistoryObject
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

    def like(self, paper_id: str, _id: str) -> Author:
        paper_operations = PaperOperations()
        paper_exist = paper_operations.find(paper_id)
        if paper_exist:
            db_author = self.find(_id)
            if paper_id not in map(lambda x: x.description, filter(lambda x: x.event == 'like', db_author.history)):
                db_author.history.append(db.HistoryObject.create_like_object(paper_id=paper_id))
                db_author.save()
                return self.to_model(db_author)
            else:
                raise HTTPException(
                    status_code=409,
                    detail='like object exist',
                )

    def delete_like(self, paper_id: str, _id: str) -> Author:
        db_author = self.find(_id)
        paper_operations = PaperOperations()
        paper_exist = paper_operations.find(paper_id)
        if paper_exist:
            if paper_id in map(lambda x: x.description, filter(lambda x: x.event == 'like', db_author.history)):
                self.collection.find_one_and_update({"_id": _id},
                                                    {"$pull": {'history': {"description": paper_id}}}, upsert=False)
                return self.to_model(db_author)
            else:
                raise HTTPException(
                    status_code=404,
                    detail='like object not found',
                )

    def get_history(self, _id: str) -> list[HistoryObject]:
        db_author = self.find(_id)
        return [HistoryObject.parse_raw(event.to_json()) for event in db_author.history]

    def get_liked_papers(self, _id: str) -> list[str]:
        history = self.get_history(_id=_id)
        liked_papers = list(map(lambda x: x.description, filter(lambda x: x.event == 'like', history)))
        return liked_papers

    @lru_cache(0)
    def create_graph_coauthors_by_author(self, author_id: str):
        paper_operations = PaperOperations()
        author = self.get_by_id(author_id)

        papers = author.papers
        graph = nx.Graph()
        for p in papers:
            paper = paper_operations.get_by_id(p)
            coauthors = paper_operations.authors_id_from_paper(paper.dict())
            coauthors = tuple(filter(lambda c: c != author_id, coauthors))
            graph.add_nodes_from(coauthors)
            graph.add_edges_from([(author_id, c) for c in coauthors])
        return graph

    def compute_h_index(self, author_id: str):
        """
        Возвращает индекс Хирша (h-index) запрашиваемого по ID автора.
        Определение (Вики):
        Учёный имеет индекс h, если h из его N статей цитируются как минимум h раз каждая,
        в то время как оставшиеся (N — h) статей цитируются не более чем h раз каждая
        P.S. Сама ф-я взята здесь: https://gist.github.com/restrepo/c5f8f9fd5504a3f93ae34dd10a5dd6b0

                Параметры:
                        author_id (str): уникальный ID автора

                Возвращаемое значение:
                        (int): индекс Хирша (h-index)
        """
        paper_operations = PaperOperations()
        # проверка на наличие автора – иначе эксепшн
        self.find(author_id)  # db_object класса Author(Document)

        # все статьи автора: list[Paper]
        all_author_papers = paper_operations.get_papers_by_author(author_id)
        if all_author_papers is not None:  # есть статьи
            # создаем лист кол-ва цитирований статей автора (n_citations: int): list[ints]
            citations = [0] * len(all_author_papers)  # type: List[int]
            for ind_paper, author_paper in enumerate(all_author_papers):
                paper_n_citations = paper_operations.get_n_citations(author_paper.id)
                citations[ind_paper] = paper_n_citations
            return sum(x >= i + 1 for i, x in enumerate(sorted(citations, reverse=True)))
        else:
            return 0
