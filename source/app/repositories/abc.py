import abc
from pydantic import BaseModel

class Repository(abc.ABC):

    @abc.abstractmethod
    def add(self, obj_in: BaseModel):
        pass

    @abc.abstractmethod
    def get_one(self, model_id: int):
        pass

    @abc.abstractmethod
    def get_all(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def update(self, model_id: int, obj_in: BaseModel):
        pass

    @abc.abstractmethod
    def delete(self, model_id: int):
        pass

class AsyncRepository(abc.ABC):

    @abc.abstractmethod
    async def add(self, obj_in: BaseModel):
        pass

    @abc.abstractmethod
    async def get_one(self, model_id: int):
        pass

    @abc.abstractmethod
    async def get_all(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def update(self, model_id: int, obj_in: BaseModel):
        pass

    @abc.abstractmethod
    async def delete(self, model_id: int):
        pass
