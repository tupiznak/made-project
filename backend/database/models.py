from pydantic import BaseModel, Field


class Paper(BaseModel):
    id: str = Field(alias='_id')
    title: str = None
    abstract: str = None
