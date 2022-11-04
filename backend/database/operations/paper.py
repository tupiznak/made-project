from typing import List, Union
try:
    import backend.database.db_objects.paper as db
    from backend.database.models.paper import *
    from backend.database.connection import citations_db
except ModuleNotFoundError:
    import database.db_objects.paper as db
    from database.models.paper import *
    from database.connection import citations_db
from mongoengine import QuerySet
from pymongo.database import Database


class PaperOperations:

    def __init__(self, database: Database = citations_db):
        self.db = database

    @property
    def collection(self):
        return self.db['paper']

    def flush(self):
        self.db.drop_collection('paper')

    def to_model(self, db_paper: Union[db.Paper, dict]) -> Paper:
        if isinstance(db_paper, db.Paper):
            return Paper.parse_raw(db_paper.to_json())
        else:
            return Paper.parse_obj(db_paper)

    def replace_id(self, paper: dict):
        paper['_id'] = paper['id']
        del paper['id']
        return paper

    def model_to_db(self, paper: Paper) -> db.Paper:
        return db.Paper(**paper.dict(by_alias=True))

    def create(self, paper: Paper) -> Paper:
        db_paper = self.model_to_db(paper)
        db_paper.save(force_insert=True)
        return paper

    def find(self, _id: str) -> db.Paper:
        return db.Paper.objects.get(_id=_id)

    def get_by_id(self, _id: str) -> Paper:
        db_paper = self.find(_id)
        paper = self.to_model(db_paper)
        return paper

    def full_update(self, paper: Paper) -> Paper:
        db_paper = self.model_to_db(paper)
        db_paper.save()
        return self.to_model(db_paper)

    def change_title(self, _id: str, title: str) -> Paper:
        db_paper = self.find(_id)
        db_paper.title = title
        db_paper.save()
        return self.to_model(db_paper)

    def get_chunk(self, id_list: List[str] = None, chunk_size: int = 10) -> List[Paper]:
        if id_list is None:
            cmd = db.Paper.objects.aggregate([{'$sample': {'size': chunk_size}}])
            db_objects = [c for c in cmd]
            papers = [self.to_model(p) for p in db_objects]
        else:
            papers = []
            for i in id_list:
                papers.append(self.get_by_id(i))
        return papers

    def delete(self, _id: str):
        paper = self.get_by_id(_id)
        self.collection.delete_one(dict(_id=paper.id))

    def base_filter(self, paper_filter: dict, exclude_paper: dict = None,
                    chunk_size: int = 10) -> List[Paper]:
        if exclude_paper is None:
            exclude_paper = {}
        exclude_paper = dict((f'{k}__ne', v) for k, v in exclude_paper.items())
        cmd = db.Paper.objects.filter(**(paper_filter | exclude_paper)) \
            .aggregate([{'$sample': {'size': chunk_size}}])
        db_objects = [c for c in cmd]
        papers = [self.to_model(p) for p in db_objects]
        return papers

    def filter(self, author: str, venue: str, year_start: int, year_end: int,
               chunk_size: int = 10) -> List[Paper]:
        match = {'year': {'$gte': year_start, '$lte': year_end}}
        if author != '':
            match['authors'] = author
        if venue != '':
            match['venue'] = venue
        query = self.collection.aggregate([
            {'$match': match},
            {'$sample': {'size': chunk_size}}
        ])
        db_objects = [o for o in query]
        papers = [self.to_model(p) for p in db_objects]
        return papers

    def find_sub_string_in_abstract(self, sub_str: str, chunk_size: int = 10) -> List[Paper]:
        query: QuerySet = db.Paper.objects(abstract__icontains=sub_str) \
            .aggregate([{'$sample': {'size': chunk_size}}])
        db_objects = [o for o in query]
        papers = [self.to_model(p) for p in db_objects]
        return papers

    def total_size(self):
        return self.collection.estimated_document_count()

    def get_papers_by_venue(self, venue_id: str, chunk_size: int = 10) -> List[Paper]:
        query = self.collection.aggregate([
            {
                '$match': {
                    'venue': venue_id
                }
            },
            {
                '$sample': {
                    'size': chunk_size
                }
            }
        ])
        db_objects = [o for o in query]
        papers = [self.to_model(p) for p in db_objects]
        return papers

    def get_papers_by_author(self, author_id: str) -> List[Paper]:
        """
        Возвращает статьи данного автора по его ID.

                Параметры:
                        author_id (str): уникальный ID автора

                Возвращаемое значение:
                        papers (list(Paper)): список статей автора
        """
        query = db.Paper.objects(authors=author_id)
        db_objects = [o for o in query]
        papers = [self.to_model(p) for p in db_objects]
        return papers

    def get_n_citations(self, paper_id: str):
        """
        Возвращает количество цитирований статьи по ее ID.

                Параметры:
                        paper_id (str): уникальный ID статьи

                Возвращаемое значение:
                        this_n_citation (int): количество цитирований статьи
        """
        db_paper = self.find(paper_id)  # Paper(Document)
        this_n_citation = db_paper.n_citation
        if this_n_citation is None:
            # предполагаем 0-ое цитирование для статей без поля 'n_citations'
            return 0
        else:
            return this_n_citation


if __name__ == '__main__':
    pass
