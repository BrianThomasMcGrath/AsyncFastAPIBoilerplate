
from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from app.database.models.base import Base


class User(Base, SQLAlchemyBaseUserTable):
    __tablename__ = "user"
