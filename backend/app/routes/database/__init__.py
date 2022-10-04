from fastapi import APIRouter
from .paper import paper_router
from .author import author_router
from .venue import venue_router

database_router = APIRouter(prefix='/database')
database_router.include_router(paper_router)
database_router.include_router(author_router)
database_router.include_router(venue_router)
