import json

from fastapi import FastAPI
import os
import datetime
from mongoengine import *

connect(name='test', host=os.environ.get('MONGODB_URI', None) or 'database')


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
        "message": json.dumps(contents)
    }
