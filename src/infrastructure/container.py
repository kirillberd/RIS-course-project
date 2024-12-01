from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from infrastructure.repositories.billboard_repository import BillboardRepository
from infrastructure.repositories.user_repository import UserRepository
from application.services.auth_service import AuthService

class Container(DeclarativeContainer):
    config = providers.Configuration()

    mysql_cm_config: MysqlCMConfig = providers.Singleton(
        MysqlCMConfig,
        host = config.db_host,
        user = config.db_user,
        password = config.db_password,
        database = config.db_name
    )

    billboard_repo: BillboardRepository = providers.Singleton(
        BillboardRepository,
        config = mysql_cm_config
    )

    user_repo: UserRepository = providers.Singleton(
        UserRepository,
        config = mysql_cm_config
    )

    auth_service: AuthService = providers.Singleton(
        AuthService,
        user_repository = user_repo,
    )



