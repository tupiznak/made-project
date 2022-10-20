from mongoengine import *
from datetime import datetime


class HistoryObject(EmbeddedDocument):
    event = StringField()
    time = IntField()
    description = StringField()

    @classmethod
    def create_like_object(cls, paper_id: str):
        return cls(event='like',
                   time=datetime.now().timestamp(),
                   description=paper_id)


class Author(Document):
    _id = StringField()
    name = StringField()
    org = StringField()
    gid = StringField()
    oid = StringField()
    orgid = StringField()
    papers = ListField(StringField())
    history = EmbeddedDocumentListField(HistoryObject)

    meta = {'strict': False, 'db_alias': 'citations'}
