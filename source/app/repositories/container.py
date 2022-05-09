from dependency_injector import containers, providers
from app.repositories.mysql import MySQLAsyncRepository

from app.database.models import Game, Team, UserTeam, User
from app.database.session import get_db


class RepositoryContainer(containers.DeclarativeContainer):

    session_factory = providers.Coroutine(get_db)

    game = providers.Factory(MySQLAsyncRepository, model=Game)
    team = providers.Factory(MySQLAsyncRepository, model=Team)
    user_team = providers.Factory(
        MySQLAsyncRepository, model=UserTeam)
    user = providers.Factory(MySQLAsyncRepository, model=User)
