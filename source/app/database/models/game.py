from re import T
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from app.database.models.base import Base


class Game(Base):
    __tablename__ = "game"

    id = Column(GUID, primary_key=True, nullable=False)
    team_1_id = Column(GUID, ForeignKey("team"))
    team_1 = relationship("Team", foreign_keys=[team_1_id])
    team_2_id = Column(GUID, ForeignKey("team"))
    team_2 = relationship("Team", foreign_keys=[team_2_id])
    score_1 = Column(Integer)
    score_2 = Column(Integer)
