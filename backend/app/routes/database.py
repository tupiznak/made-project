from fastapi import APIRouter

from database.models import Paper
from database.operations import PaperOperations

database_router = APIRouter()


@database_router.post("/database/papers/create", tags=['papers'])
async def create_database_paper(paper: Paper):
    return PaperOperations.create(paper)


@database_router.post("/database/papers/read", tags=['papers'])
async def read_database_paper(_id: str):
    return PaperOperations.get_by_id(_id=_id)


@database_router.post("/database/papers/update", tags=['papers'])
async def update_database_paper(paper: Paper):
    return PaperOperations.full_update(paper)


@database_router.post("/database/papers/update/title", tags=['papers'])
async def update_database_paper(_id: str, title: str):
    return PaperOperations.change_title(_id, title)


@database_router.post("/database/papers/delete", tags=['papers'])
async def update_database_paper(_id: str):
    return PaperOperations.delete(_id)


@database_router.get("/database/papers/", tags=['papers'])
async def read_database_papers(chunk_size: int = 10):
    return PaperOperations.get_chunk(chunk_size=chunk_size)


@database_router.post("/database/papers/filter", tags=['papers'])
async def filter_database_papers(paper_filter: dict, exclude_paper: dict = None, chunk_size: int = 10):
    return PaperOperations.filter(paper_filter=paper_filter, exclude_paper=exclude_paper, chunk_size=chunk_size)


@database_router.post("/database/papers/abstract_substring", tags=['papers'])
async def sub_str_in_abstract_database_papers(sub_string: str, chunk_size: int = 10):
    return PaperOperations.find_sub_string_in_abstract(sub_str=sub_string, chunk_size=chunk_size)
