from mongoengine import *


class Paper(Document):
    _id = StringField()
    title = StringField()
    abstract = StringField()
    year = IntField()
    n_citation = IntField()
    venue = StringField()
    authors = ListField(StringField())

    meta = {'strict': False, 'db_alias': 'citations'}
