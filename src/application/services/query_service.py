from dataclasses import dataclass
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.billboard_repository import BillboardRepository
from infrastructure.providers.sql_provider import SQLProvider
from domain.queries import UserQuery, OwnerBillboardsQuery
import logging

module_logger = logging.getLogger(__name__)


@dataclass
class QueryService:
    user_repository: UserRepository
    billboard_repository: BillboardRepository
    sql_provider: SQLProvider



    def get_customers(self, year, month):
        query = self.sql_provider.get("get_customer.sql", year=year, month=month)
        result = self.user_repository.get_many(query, validate=False)
        return result

    def get_billboards(self, year, month, lastname):
        query = self.sql_provider.get("get_billboards.sql", year=year, month=month, lastname=lastname)
        result = self.billboard_repository.get_info(query)
        return result
