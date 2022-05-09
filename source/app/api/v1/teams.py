from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from app.schema.team import TeamIn
from app.container import Container
from app.services.crud.base import BaseAsyncCrudService


router = APIRouter()


@router.get("/teams")
@inject
async def fetch_teams(team_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.team])):
    return await team_service.get_all()


@router.post("/teams")
@inject
async def create_team(obj_in: TeamIn, team_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.team])):
    return await team_service.add(obj_in)


@router.get("/teams/{id}")
@inject
async def fetch_one_team(id: int, team_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.team])):
    return await team_service.get_one(id)


@router.put("/teams/{id}")
@inject
async def update_team(id: int, obj_in: TeamIn, team_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.team])):
    return await team_service.update(id, obj_in)


@router.delete("/teams/{id}")
@inject
async def delete_team(id: int, team_service: BaseAsyncCrudService = Depends(Provide[Container.service.crud.team])):
    return await team_service.delete(id)
