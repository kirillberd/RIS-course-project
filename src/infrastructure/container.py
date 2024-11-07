from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from infrastructure.repositories.billboard_repository import BillboardRepository

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

