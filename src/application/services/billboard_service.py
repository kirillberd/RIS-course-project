from dataclasses import dataclass
from infrastructure.repositories.billboard_repository import BillboardRepository
from infrastructure.providers.sql_provider import SQLProvider
from domain.billboards import BillboardQuery

@dataclass
class BillboardService:
    sql_provider: SQLProvider
    billboard_repository: BillboardRepository


    def get_billboards(self, query_obj: BillboardQuery):
        conditions_dict = self._make_query_conditions(query_obj)
        query = self.sql_provider.get("get_billboards.sql", **conditions_dict)
        self.billboard_repository.get(query)

    def _make_query_conditions(self, query_obj: BillboardQuery) -> dict:
        conditions = {}
        if query_obj.city:
            conditions['city_clause'] = f"AND city LIKE '%{query_obj.city}%'"
        if query_obj.direction:
            conditions['direction_clause'] = f"AND direction LIKE '%{query_obj.direction}%'"
        if query_obj.cost_min:
            conditions['cost_min_clause'] = f"AND cost >= {query_obj.cost_min}"
        if query_obj.cost_max:
            conditions['cost_max_clause'] = f"AND cost <= {query_obj.cost_max}"
        if query_obj.size_min:
            conditions['size_min_clause'] = f"AND size >= {query_obj.size_min}"
        if query_obj.size_max:
            conditions['size_max_clause'] = f"AND size <= {query_obj.size_max}"
        if query_obj.min_quality:
            conditions['quality_clause'] = f"AND quality_indicator >= {query_obj.min_quality}"
        if query_obj.address:
            conditions['address_clause'] = f"AND addres LIKE '%{query_obj.address}%'"
        if query_obj.date_from:
            conditions['date_from_clause'] = f"AND installation_date >= '{query_obj.date_from}'"
        if query_obj.date_to:
            conditions['date_to_clause'] = f"AND installation_date <= '{query_obj.date_to}'"
        default_conditions = [
            'city_clause', 'direction_clause', 
            'cost_min_clause', 'cost_max_clause',
            'size_min_clause', 'size_max_clause', 
            'quality_clause', 'address_clause',
            'date_from_clause', 'date_to_clause'
        ]
        for condition in default_conditions:
            if condition not in conditions:
                conditions[condition] = ''
        return conditions
