from telnetlib import GA
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from app.schema.game import GameIn
from app.container import Container
from app.services.crud.base import BaseAsyncCrudService


router = APIRouter()


@router.get("/games")
@inject
async def fetch_games(game_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.game])):
    return await game_service.get_all()


@router.post("/games")
@inject
async def create_game(obj_in: GameIn, game_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.game])):
    return await game_service.add(obj_in)


@router.get("/games/{id}")
@inject
async def fetch_one_game(id: int, game_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.game])):
    return await game_service.get_one(id)


@router.put("/games/{id}")
@inject
async def update_game(id: int, obj_in: GameIn, game_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.game])):
    return await game_service.update(id, obj_in)


@router.delete("/games/{id}")
@inject
async def delete_game(id: int, game_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.game])):
    return await game_service.delete(id)
