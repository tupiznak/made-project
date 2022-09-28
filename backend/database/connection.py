import os

from mongoengine import *
from pymongo import MongoClient

try:
    host = os.environ['MONGODB_URI']
    host = host.rsplit('/', maxsplit=1)[0] + '/user'
except KeyError:
    host = 'database'


def new_connection() -> MongoClient:
    return connect(name='citations', host=host)


client = new_connection()
citations_db = client['citations']


class Paper(Document):
    _id = StringField(required=True)
    title = StringField()
    abstract = StringField()
    meta = {'strict': False}
