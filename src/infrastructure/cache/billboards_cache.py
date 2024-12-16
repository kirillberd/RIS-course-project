from redis import Redis
import json
from datetime import timedelta, datetime
from dataclasses import dataclass
from domain.billboards import Billboard, BillboardQuery
from typing import List, Optional

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

@dataclass
class BillboardsCache:
    redis_client: Redis
    cache_ttl: timedelta

    def get_key(self, query: BillboardQuery) -> str:
        query_dict = query.model_dump()
        sorted_params = sorted(
            (k, v) for k, v in query_dict.items() 
            if v is not None
        )
        return f"billboards:{hash(frozenset(sorted_params))}"

    def get_billboards(self, query: BillboardQuery) -> Optional[List[Billboard]]:
        key = self.get_key(query)
        data = self.redis_client.get(key)
        
        if data:
            billboards_data = json.loads(data)
            return [Billboard(**b) for b in billboards_data]
        return None

    def set_billboards(self, query: BillboardQuery, billboards: List[Billboard]):
        key = self.get_key(query)
        billboards_data = [b.model_dump() for b in billboards]
        
        self.redis_client.setex(
            key,
            self.cache_ttl,
            json.dumps(billboards_data, cls=DateTimeEncoder)
        )