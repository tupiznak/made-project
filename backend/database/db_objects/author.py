from mongoengine import *


class HistoryObject(EmbeddedDocument):
    event = StringField()
    event_time = DateTimeField()
    event_description = StringField()


class Author(Document):
    _id = StringField()
    name = StringField()
    org = StringField()
    gid = StringField()
    oid = StringField()
    orgid = StringField()
    papers = ListField(StringField)
    history = EmbeddedDocumentListField(HistoryObject)

    meta = {'strict': False, 'db_alias': 'citations'}
