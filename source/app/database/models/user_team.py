from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from app.database.models.base import Base


class UserTeam(Base):
    __tablename__ = "user_team"

    user_id = Column(GUID, ForeignKey("user.id"),
                     nullable=False, primary_key=True)
    user = relationship("User")
    team_id = Column(GUID, ForeignKey("team.id"),
                     nullable=False, primary_key=True)
    team = relationship("Team")
