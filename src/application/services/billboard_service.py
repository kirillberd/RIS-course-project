from dataclasses import dataclass
from infrastructure.repositories.billboard_repository import BillboardRepository
from infrastructure.providers.sql_provider import SQLProvider
from domain.billboards import BillboardQuery, Billboard
from typing import List
from infrastructure.cache.billboards_cache import BillboardsCache
import logging

module_logger = logging.getLogger(__name__)


@dataclass
class BillboardService:
    sql_provider: SQLProvider
    billboard_repository: BillboardRepository
    billboards_cache: BillboardsCache

    def get_billboards(self, query_obj: BillboardQuery) -> List[Billboard]:

        cached_billboards = self.billboards_cache.get_billboards(query_obj)
        if cached_billboards:
            module_logger.info("Return cached billboards!")
            return cached_billboards

        conditions_dict = self._make_query_conditions(query_obj)
        query = self.sql_provider.get("get_billboards.sql", **conditions_dict)

        billboards = self.billboard_repository.get(query)
        self.billboards_cache.set_billboards(query_obj, billboards)
        return billboards

    def add_billboard(self, billboard: Billboard) -> None:
        query = self.sql_provider.get("add_billboard.sql", **billboard.model_dump())
        self.billboard_repository.add(query)

    def get_billboard_by_id(self, billboard_id) -> Billboard:
        query = self.sql_provider.get(
            "get_billboard_by_id.sql", billboard_id=billboard_id
        )
        return self.billboard_repository.get(query)[0]

    def _make_query_conditions(self, query_obj: BillboardQuery) -> dict:
        conditions = {}

        conditions["schedule_clause"] = f"""
            AND b.id NOT IN (
            SELECT billboard_id
            FROM schedule
            WHERE (
            (date_begin < '{query_obj.date_end}' AND date_end >= '{query_obj.date_start}')
            )
            )
            """

        if query_obj.city:
            conditions["city_clause"] = f"AND b.city LIKE '%{query_obj.city}%'"

        if query_obj.direction:
            conditions["direction_clause"] = (
                f"AND b.direction LIKE '%{query_obj.direction}%'"
            )

        if query_obj.cost_min:
            conditions["cost_min_clause"] = f"AND b.cost >= {query_obj.cost_min}"

        if query_obj.cost_max:
            conditions["cost_max_clause"] = f"AND b.cost <= {query_obj.cost_max}"

        if query_obj.size_min:
            conditions["size_min_clause"] = f"AND b.size >= {query_obj.size_min}"

        if query_obj.size_max:
            conditions["size_max_clause"] = f"AND b.size <= {query_obj.size_max}"

        if query_obj.min_quality:
            conditions["quality_clause"] = (
                f"AND b.quality_indicator >= {query_obj.min_quality}"
            )

        if query_obj.address:
            conditions["address_clause"] = f"AND b.addres LIKE '%{query_obj.address}%'"

        default_conditions = [
            "city_clause",
            "direction_clause",
            "cost_min_clause",
            "cost_max_clause",
            "size_min_clause",
            "size_max_clause",
            "quality_clause",
            "address_clause",
            "schedule_clause",
        ]

        for condition in default_conditions:
            if condition not in conditions:
                conditions[condition] = ""

        return conditions
