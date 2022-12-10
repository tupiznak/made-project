from fastapi import Request

from fastapi import APIRouter
from .database.author import author_operations

model_router = APIRouter(prefix='/model')


@model_router.post("/predict", tags=['model'])
def model_request(request: Request):
    return 2
