from dataclasses import dataclass
from domain.billboards import Billboard
import logging
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from infrastructure.context.mysql_context_manager import MysqlContextManager
from typing import List

module_logger = logging.getLogger(__name__)

@dataclass
class BillboardRepository:
    config: MysqlCMConfig
    config_dict: dict = None

    def __post_init__(self):
        self.config_dict = self.config.model_dump()

    def add(self, billboard: Billboard):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Test")
            else:
                module_logger.info(billboard)
    def get(self, query) -> List[Billboard]:
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Test")
            else:
                
                cur.execute(query)
                result = cur.fetchall()
                billboards = []
                for row in result:
                    id_, cost, size, inst_date, address, quality, city, direction, owner_id, _ = row

                    billboard = Billboard(
                        id=id_,
                        cost=float(cost),  
                        size=float(size),
                        addres=address,
                        quality_indicator=quality,
                        city=city,
                        direction=direction,
                        billboard_owner_id=owner_id,
                        installation_date=inst_date
                    )
                    billboards.append(billboard)

                return billboards