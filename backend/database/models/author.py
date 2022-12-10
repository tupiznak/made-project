from pydantic import BaseModel, Field


class HistoryObject(BaseModel):
    event: str
    time: int
    description: str


class Author(BaseModel):
    id: str = Field(alias='_id')
    name: str = None
    h_index: int = None
    org: str = None
    gid: str = None
    oid: str = None
    orgid: str = None
    papers: list[str] = Field(default_factory=lambda: [])
    vectorized_papers: dict[str, list[float]] = Field(default_factory=lambda: {})
    history: list[HistoryObject] = Field(default_factory=lambda: [])

    def __hash__(self):
        return hash(self.id)
