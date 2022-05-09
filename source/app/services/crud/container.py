from dependency_injector import containers, providers
from app.repositories.container import RepositoryContainer
from app.services.crud.base import BaseAsyncCrudService


class CrudServiceContainer(
    containers.DeclarativeContainer
):
    game = providers.Factory(
        BaseAsyncCrudService, repository=RepositoryContainer.game)
    team = providers.Factory(
        BaseAsyncCrudService, repository=RepositoryContainer.team)
    user_team = providers.Factory(
        BaseAsyncCrudService, repository=RepositoryContainer.user_team)
    user = providers.Factory(
        BaseAsyncCrudService, repository=RepositoryContainer.user)
