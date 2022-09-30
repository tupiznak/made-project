from fastapi import APIRouter

from database.models import Paper
from database.operations import PaperOperations

database_router = APIRouter()

paper_operations = PaperOperations()


@database_router.post("/database/papers/create", tags=['papers'])
async def create_database_paper(paper: Paper):
    return paper_operations.create(paper)


@database_router.post("/database/papers/read", tags=['papers'])
async def read_database_paper(_id: str):
    return paper_operations.get_by_id(_id=_id)


@database_router.post("/database/papers/update", tags=['papers'])
async def update_database_paper(paper: Paper):
    return paper_operations.full_update(paper)


@database_router.post("/database/papers/update/title", tags=['papers'])
async def update_title_database_paper(_id: str, title: str):
    return paper_operations.change_title(_id, title)


@database_router.post("/database/papers/delete", tags=['papers'])
async def delete_database_paper(_id: str):
    return paper_operations.delete(_id)


@database_router.get("/database/papers/", tags=['papers'])
async def read_database_papers(chunk_size: int = 10):
    return paper_operations.get_chunk(chunk_size=chunk_size)


@database_router.post("/database/papers/filter", tags=['papers'])
async def filter_database_papers(paper_filter: dict, exclude_paper: dict = None, chunk_size: int = 10):
    return paper_operations.filter(paper_filter=paper_filter, exclude_paper=exclude_paper, chunk_size=chunk_size)


@database_router.post("/database/papers/abstract_substring", tags=['papers'])
async def sub_str_in_abstract_database_papers(sub_string: str, chunk_size: int = 10):
    return paper_operations.find_sub_string_in_abstract(sub_str=sub_string, chunk_size=chunk_size)


@database_router.get("/database/papers/total_size", tags=['papers'])
async def total_size_database_papers():
    return paper_operations.total_size()
