from typing import Generic, TypeVar

from pydantic import BaseModel

from app.database.models.base import Base
from app.database.session import database
from app.repositories.abc import AsyncRepository


class BaseAsyncCrudService:

    def __init__(self, repository: AsyncRepository):
        self._repository: AsyncRepository = repository

    async def add(self, obj_in: BaseModel):
        return await self._repository.add(obj_in)

    async def get_one(self, model_id: int):
        return await self._repository.get_one(model_id)

    async def get_all(self):
        return await self._repository.get_all()

    async def update(self, model_id: int, obj_in: BaseModel):
        return await self._repository.update(model_id, obj_in)

    async def delete(self, model_id: int):
        await self._repository.delete(model_id)
