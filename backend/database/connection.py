import os

from mongoengine import *
from pymongo import MongoClient
from pymongo.database import Database

DATABASE_NAME = 'citations'


def new_connection(db_name: str = None) -> (MongoClient, Database):
    db_name = db_name or DATABASE_NAME
    try:
        host = os.environ['MONGODB_URI']
        host = host.rsplit('/', maxsplit=1)[0] + '/' + db_name
    except KeyError:
        host = 'database'
    db_client = connect(name=db_name, host=host)
    return db_client, db_client[db_name]


client, citations_db = new_connection()
