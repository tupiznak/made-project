from mongoengine import *


class Paper(Document):
    _id = StringField()
    title = StringField()
    abstract = StringField()
    year = IntField()

    meta = {'strict': False, }
