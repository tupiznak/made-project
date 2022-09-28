from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import connect

_ = connect

app = FastAPI()

origins = [
    "http://frontend:3000",
    "http://127.0.0.1:3000",
    "https://made22t4.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }


@app.get("/db/create", tags=["Root"])
async def db_create():
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }


@app.get("/db/read")
async def db_read():
    contents = []
    for post in BlogPost.objects:
        contents.append(post.content)

    return {
        "message": len(contents)
    }
