from pydantic import BaseModel, Field
from datetime import datetime


class HistoryObject(BaseModel):
    event: str = None
    event_time: datetime = None
    event_description: str = None


class Author(BaseModel):
    id: str = Field(alias='_id')
    name: str = None
    org: str = None
    gid: str = None
    oid: str = None
    orgid: str = None
    history: list[HistoryObject] = Field(default_factory=lambda: [])

    def __hash__(self):
        return hash(self.id)
