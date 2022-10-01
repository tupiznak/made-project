from pydantic import BaseModel, Field


class Paper(BaseModel):
    id: str = Field(alias='_id')
    title: str = None
    abstract: str = None
    year: int = None
    n_citation: int = None
    venue: str = None
    authors: list[str] = Field(default_factory=lambda: [])

    def __hash__(self):
        return hash(self.id)
