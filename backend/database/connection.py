import os

from mongoengine import *
from pymongo import MongoClient
from pymongo.database import Database

DATABASE_NAME = 'citations'


def new_connection(db_name: str = None, alias: str = None) -> tuple[MongoClient, Database]:
    db_name = db_name or DATABASE_NAME
    alias = alias or db_name
    try:
        host = os.environ['MONGODB_URI']
        host = host.rsplit('/', maxsplit=1)[0] + '/' + db_name
    except KeyError:
        host = 'databasegit'
    db_client = connect(name=db_name, host=host, alias=alias)
    return db_client, db_client[db_name]


def disconnect_database(alias: str):
    disconnect(alias=alias)


client, citations_db = new_connection()
