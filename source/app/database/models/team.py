
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from app.database.models.base import Base


class Team(Base):
    __tablename__ = "team"

    id = Column(GUID, primary_key=True)
    name = Column(String(32), nullable=False)
    city_town = Column(String(32))
