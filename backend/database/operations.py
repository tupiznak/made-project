from typing import List, Union

import database.db_objects as db
from .models import *
from .connection import citations_db

_ = citations_db


class PaperOperations:

    @staticmethod
    def flush():
        citations_db.drop_collection('paper')

    @staticmethod
    def to_model(db_paper: Union[db.Paper, dict]) -> Paper:
        if isinstance(db_paper, db.Paper):
            return Paper.parse_raw(db_paper.to_json())
        else:
            return Paper.parse_obj(db_paper)

    @staticmethod
    def replace_id(paper: dict):
        paper['_id'] = paper['id']
        del paper['id']
        return paper

    @staticmethod
    def model_to_db(paper: Paper) -> db.Paper:
        return db.Paper(**paper.dict(by_alias=True))

    @staticmethod
    def create(paper: Paper) -> Paper:
        db_paper = PaperOperations.model_to_db(paper)
        db_paper.save(force_insert=True)
        return paper

    @staticmethod
    def find(_id: str) -> db.Paper:
        return db.Paper.objects.get(_id=_id)

    @staticmethod
    def get_by_id(_id: str) -> Paper:
        db_paper = PaperOperations.find(_id)
        paper = PaperOperations.to_model(db_paper)
        return paper

    @staticmethod
    def full_update(paper: Paper) -> Paper:
        db_paper = PaperOperations.model_to_db(paper)
        db_paper.save()
        return PaperOperations.to_model(db_paper)

    @staticmethod
    def change_title(_id: str, title: str) -> Paper:
        db_paper = PaperOperations.find(_id)
        db_paper.title = title
        db_paper.save()
        return PaperOperations.to_model(db_paper)

    @staticmethod
    def get_chunk(id_list: List[str] = None, chunk_size: int = 10) -> List[Paper]:
        if id_list is None:
            cmd = db.Paper.objects.aggregate([{'$sample': {'size': chunk_size}}])
            db_objects = [c for c in cmd]
            papers = [PaperOperations.to_model(p) for p in db_objects]
        else:
            papers = []
            for i in id_list:
                papers.append(PaperOperations.get_by_id(i))
        return papers

    @staticmethod
    def filter(paper_filter: dict, exclude_paper: dict = None, chunk_size: int = 10) -> List[Paper]:
        if exclude_paper is None:
            exclude_paper = {}
        exclude_paper = dict((f'{k}__ne', v) for k, v in exclude_paper.items())
        cmd = db.Paper.objects.filter(**(paper_filter | exclude_paper)) \
            .aggregate([{'$sample': {'size': chunk_size}}])
        db_objects = [c for c in cmd]
        papers = [PaperOperations.to_model(p) for p in db_objects]
        return papers

    @staticmethod
    def delete(_id: str):
        paper = PaperOperations.get_by_id(_id)
        citations_db['paper'].delete_one(dict(_id=paper.id))


if __name__ == '__main__':
    pass
