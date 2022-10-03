from pydantic import BaseModel, Field


class Venue(BaseModel):
    id: str = Field(alias='_id')
    name_d: str = None
    raw: str = None
    type: str = None

    def __hash__(self):
        return hash(self.id)
