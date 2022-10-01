from mongoengine import *

from .venue import Venue


class Paper(Document):
    _id = StringField()
    title = StringField()
    abstract = StringField()
    year = IntField()
    n_citation = IntField()
    venue = Venue()

    meta = {'strict': False, 'db_alias': 'citations'}
