from pydantic import BaseModel, Field


class HistoryObject(BaseModel):
    event: str
    time: int
    description: str


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
