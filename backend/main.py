import mongoengine.errors
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette_exporter import PrometheusMiddleware

from app.routes.database import database_router
from app.routes.metrics import metric_request
from database.connection import connect

_ = connect


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
    "*"
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

from fastapi.responses import HTMLResponse
@app.get("/test", response_class=HTMLResponse)
async def test():
    return HTMLResponse(content='<html><h1>test</h1></html>', status_code=200)
