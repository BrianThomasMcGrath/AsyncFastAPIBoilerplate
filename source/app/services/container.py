from dependency_injector import containers, providers

from app.services.crud.container import CrudServiceContainer


class ServiceContainer(containers):
    crud = providers.Container(CrudServiceContainer)
