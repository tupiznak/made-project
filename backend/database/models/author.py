from pydantic import BaseModel, Field


class Author(BaseModel):
    id: str = Field(alias='_id')
    name: str = None
    org: str = None
    gid: str = None
    oid: str = None
    orgid: str = None

    def __hash__(self):
        return hash(self.id)
