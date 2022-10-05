import mongoengine.errors
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Gauge
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.routes.database import database_router
from database.connection import connect

from app.routes.database.paper import paper_operations
from app.routes.database.author import author_operations
from app.routes.database.venue import venue_operations

_ = connect

papers_count = Gauge('papers_count', 'Count of papers')
author_count = Gauge('author_count', 'Count of author')
venue_count = Gauge('venue_count', 'Count of venue')


def metric_request(request: Request):
    papers_count.set(paper_operations.total_size())
    author_count.set(author_operations.total_size())
    venue_count.set(venue_operations.total_size())
    return handle_metrics(request)


app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metric_request)


@app.exception_handler(mongoengine.errors.NotUniqueError)
async def validation_exception_handler(request, err):
    return JSONResponse(status_code=409, content=f'{dict(message="object exist")}')


@app.exception_handler(mongoengine.errors.DoesNotExist)
async def validation_exception_handler(request, err):
    return JSONResponse(status_code=404, content=f'{dict(message="object does not exist")}')


origins = [
    "http://frontend:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://made22t4.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(database_router)


@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }
