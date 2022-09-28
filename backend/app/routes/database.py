import mongoengine.errors
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


@database_router.get("/database/papers/", tags=['papers'])
async def read_database_papers():
    return PaperOperations.get_chunk()
