import uuid
from typing import List, Optional


from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import UUID4


class TeamBase(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: Optional[str]
    city_town: Optional[str]


class TeamIn(BaseModel):
    name: str
    city_town: str


class TeamResponse(TeamBase):

    class Config:
        orm_mode = True
