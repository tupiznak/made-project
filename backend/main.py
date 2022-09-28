import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mongoengine import *
from database.connection import connect

_ = connect


class BlogPost(Document):
    title = StringField(required=True, max_length=200)
    posted = DateTimeField(default=datetime.datetime.utcnow)
    tags = ListField(StringField(max_length=50))
    meta = {'allow_inheritance': True}


class TextPost(BlogPost):
    content = StringField(required=True)


class LinkPost(BlogPost):
    url = StringField(required=True)


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
    post1 = TextPost(title='Using MongoEngine', content='See the tutorial')
    post1.tags = ['mongodb', 'mongoengine']
    post1.save()

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
