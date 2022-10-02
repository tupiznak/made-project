from mongoengine import *


class Venue(Document):
    _id = StringField()
    name_d = StringField()
    raw = StringField()
    type = IntField()

    meta = {'strict': False, 'db_alias': 'citations'}
