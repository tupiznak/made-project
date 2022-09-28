from mongoengine import *


class Paper(Document):
    _id = StringField()
    title = StringField()
    abstract = StringField()
    year = IntField()
    n_citation = IntField()

    meta = {'strict': False, }
