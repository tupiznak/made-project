from mongoengine import *


class Author(Document):
    _id = StringField()
    name = StringField()
    org = StringField()
    gid = StringField()
    oid = StringField()
    orgid = StringField()
    papers = ListField(StringField)

    meta = {'strict': False, 'db_alias': 'citations'}
