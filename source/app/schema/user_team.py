

from typing import Optional
import uuid
from pydantic.main import BaseModel
from pydantic.types import UUID4


class UserTeamBase(BaseModel):
    user_id: Optional[UUID4]
    team_id: Optional[UUID4]


class UserTeamResponse(BaseModel):
    class Config:
        orm_mode = True
