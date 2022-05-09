from dependency_injector import containers, providers
from app.services.container import ServiceContainer


class Container(containers.DeclarativeContainer):
    service = providers.Container(ServiceContainer)
