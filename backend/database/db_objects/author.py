from mongoengine import *


class Author(Document):
    _id = StringField()
    name = StringField()
    org = StringField()  # organization name?
    gid = StringField()  # ?
    oid = StringField()  # ?
    orgid = StringField()  # organozation id?
    papers = ListField(StringField)  # list of paper id's

    meta = {'strict': False, 'db_alias': 'citations'}
