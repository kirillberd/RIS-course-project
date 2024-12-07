from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from infrastructure.repositories.billboard_repository import BillboardRepository
from infrastructure.repositories.user_repository import UserRepository
from application.services.auth_service import AuthService
from infrastructure.providers.sql_provider import SQLProvider
from application.services.billboard_service import BillboardService
from application.services.query_service import QueryService
from pathlib import Path

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

    billboard_sql_provider: SQLProvider = providers.Singleton(
        SQLProvider,
        Path(__file__).parent / "sql" / "billboards"
    )

    billboard_service: BillboardService = providers.Singleton(
        BillboardService,
        sql_provider = billboard_sql_provider,
        billboard_repository = billboard_repo
    )

    user_repo: UserRepository = providers.Singleton(
        UserRepository,
        config = mysql_cm_config
    )

    auth_sql_provider: SQLProvider = providers.Singleton(
        SQLProvider,
        Path(__file__).parent / "sql" / "auth"

    )
    auth_service: AuthService = providers.Singleton(
        AuthService,
        user_repository = user_repo,
        sql_provider = auth_sql_provider
    )

    query_sql_provider: SQLProvider = providers.Singleton(
        SQLProvider,
        Path(__file__).parent / "sql" / "queries"
    )
    query_service: QueryService = providers.Singleton(
        QueryService,
        user_repository = user_repo,
        billboard_repository = billboard_repo,
        sql_provider = query_sql_provider
    )



