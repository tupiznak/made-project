import os

from mongoengine import *
from pymongo import MongoClient

DATABASE_NAME = 'citations'

try:
    host = os.environ['MONGODB_URI']
    host = host.rsplit('/', maxsplit=1)[0] + '/user'
except KeyError:
    host = 'database'


def new_connection() -> MongoClient:
    return connect(name=DATABASE_NAME, host=host)


client = new_connection()
citations_db = client[DATABASE_NAME]
