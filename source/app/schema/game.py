from typing import Optional
import uuid
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import UUID4


class GameBase(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    team_1_id: Optional[UUID4]
    team_2_id: Optional[UUID4]
    score_1: Optional[int] = 0
    score_2: Optional[int] = 0


class GameIn(BaseModel):
    team_1_id: UUID4
    team_2_id: UUID4


class GameResponse(GameBase):
    class Config:
        orm_mode = True
