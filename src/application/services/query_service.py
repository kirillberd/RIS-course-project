from dataclasses import dataclass
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.billboard_repository import BillboardRepository
from infrastructure.providers.sql_provider import SQLProvider
from domain.queries import UserQuery
import logging

module_logger = logging.getLogger(__name__)


@dataclass
class QueryService:
    user_repository: UserRepository
    billboard_repository: BillboardRepository
    sql_provider: SQLProvider



    def get_users(self, user_query: UserQuery):
        conditions = self._make_user_query_conditions(user_query)
        query = self.sql_provider.get("get_users.sql", **conditions)
        result = self.user_repository.get_many(query)
        return result
    def _make_user_query_conditions(self, query_obj: UserQuery) -> dict:
        conditions = {}
   

        if query_obj.role == "analyst":
            conditions["table_clause"] = f"FROM internal_users"
        elif query_obj.role:
            conditions["table_clause"] = f"FROM external_users"
        else:
            conditions["table_clause"] = f"""
                FROM (
                    SELECT * FROM internal_users 
                    UNION ALL 
                    SELECT * FROM external_users
                ) as users
            """
        if query_obj.role:
            conditions["role_clause"] = f"AND role = '{query_obj.role}'"
        else:
            conditions["role_clause"] = ""

        if query_obj.firstname:
            conditions["firstname_clause"] = f"AND firstname LIKE '%{query_obj.firstname}%'"
        else:
            conditions["firstname_clause"] = ""

        if query_obj.lastname:
            conditions["lastname_clause"] = f"AND lastname LIKE '%{query_obj.lastname}%'"
        else:
            conditions["lastname_clause"] = ""

        return conditions