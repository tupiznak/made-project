from mongoengine import *


class Venue(Document):
    _id = StringField()
    name_d = StringField()
    raw = StringField()
    type = StringField()

    meta = {'strict': False, 'db_alias': 'citations'}
