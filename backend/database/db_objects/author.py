from datetime import datetime

from mongoengine import *


class HistoryObject(EmbeddedDocument):
    event = StringField()
    time = IntField()
    description = StringField()

    @classmethod
    def create_like_object(cls, paper_id: str):
        return cls(event='like',
                   time=datetime.now().timestamp(),
                   description=paper_id)

    @classmethod
    def create_unlike_object(cls, paper_id: str):
        return cls(event='unlike',
                   time=datetime.now().timestamp(),
                   description=paper_id)


class PaperEmbedding(EmbeddedDocument):
    paper_id = StringField()
    paper_vector = ListField(FloatField())

    def to_python(self, *args):
        return {}

    def _validate(self, *args):
        return True

    def _to_mongo_safe_call(self, *args):
        return self.paper_vector


class Author(Document):
    _id = StringField()
    name = StringField()
    org = StringField()
    gid = StringField()
    oid = StringField()
    orgid = StringField()
    h_index = IntField()
    papers = ListField(StringField())
    vectorized_papers = DictField(PaperEmbedding())
    history = EmbeddedDocumentListField(HistoryObject)  # list of paper id's

    meta = {'strict': False, 'db_alias': 'citations'}
