from typing import Callable, Coroutine
from pydantic import BaseModel
from app.database.models.base import Base
from app.repositories.abc import AsyncRepository


class MySQLAsyncRepository(AsyncRepository):

    def __init__(self, model: Base, session_factory: Coroutine) -> None:
        self._model = model
        self._session_factory = session_factory

    async def add(self, obj_in: BaseModel):
        database = await self._session_factory()
        query = self._model.insert().values(**obj_in.dict())
        model_id = await database.execute(query)
        return await self.get_one(model_id)

    async def get_one(self, model_id: int):
        database = self._session_factory()
        query = self._model.select().where(id == model_id)
        return await database.fetch_one(query)

    async def get_all(self):
        database = await self._session_factory()
        query = self._model.select()
        return await database.fetch_all(query)

    async def update(self, model_id: int, obj_in: BaseModel):
        database = await self._session_factory()
        query = self._model.update().where(id == model_id).values(**obj_in.dict())
        model_id = await database.execute(query)
        return await self.get_one(model_id)

    async def delete(self, model_id: int):
        database = await self._session_factory()
        query = self._model.delete().where(id == model_id)
        model_id = await database.execute(query)
