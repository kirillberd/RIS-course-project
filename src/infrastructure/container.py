from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from infrastructure.repositories.billboard_repository import BillboardRepository
from infrastructure.repositories.user_repository import UserRepository
from application.services.auth_service import AuthService
from infrastructure.providers.sql_provider import SQLProvider
from application.services.billboard_service import BillboardService
from application.services.query_service import QueryService
from infrastructure.repositories.order_repository import OrderRepository
from application.services.order_service import OrderService
from infrastructure.cache.billboards_cache import BillboardsCache
from pathlib import Path
from datetime import timedelta
from infrastructure.repositories.report_repository import ReportRepository
from application.services.report_service import ReportService
from redis import Redis

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

    redis_client: Redis = providers.Singleton(
        Redis
    )
    cache_ttl: timedelta = providers.Singleton(
        timedelta,
        hours=1,
    )

    billboards_cache: BillboardsCache = providers.Singleton(
        BillboardsCache,
        redis_client = redis_client,
        cache_ttl = cache_ttl
    )

    billboard_service: BillboardService = providers.Singleton(
        BillboardService,
        sql_provider = billboard_sql_provider,
        billboard_repository = billboard_repo,
        billboards_cache = billboards_cache
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

    order_repo: OrderRepository = providers.Singleton(
        OrderRepository,
        config = mysql_cm_config
    )

    order_sql_provider: SQLProvider = providers.Singleton(
        SQLProvider,
        Path(__file__).parent / "sql" / "orders"
    )
    
    order_service: OrderService = providers.Singleton(
        OrderService,
        order_repository = order_repo,
        sql_provider = order_sql_provider
    )

    report_sql_provider: SQLProvider = providers.Singleton(
        SQLProvider,
        Path(__file__).parent / "sql" / "reports"
    )

    report_repo: ReportRepository = providers.Singleton(
        config = mysql_cm_config
    )

    report_service: ReportService = providers.Singleton(
        ReportService,
        sql_provider = report_sql_provider,
        report_repository = report_repo
    )

