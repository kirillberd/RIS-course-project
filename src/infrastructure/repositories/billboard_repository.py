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

    def add(self, query):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Test")
            else:
                result = cur.execute(query)
                module_logger.info(result)

    def get(self, query) -> List[Billboard]:
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Test")
            else:

                cur.execute(query)
                result = cur.fetchall()
                billboards = []
                for row in result:
                    (
                        id_,
                        cost,
                        size,
                        inst_date,
                        address,
                        quality,
                        city,
                        direction,
                        owner_id,
                        _,
                    ) = row

                    billboard = Billboard(
                        id=id_,
                        cost=float(cost),
                        size=float(size),
                        addres=address,
                        quality_indicator=quality,
                        city=city,
                        direction=direction,
                        billboard_owner_id=owner_id,
                        installation_date=inst_date,
                    )
                    billboards.append(billboard)

                return billboards

    def get_info(self, query):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Test")
            else:
                cur.execute(query)
                result = cur.fetchall()
                info_list = []
                for info in result:
                    info_dict = dict(
                        [(item[0], info[i]) for i, item in enumerate(cur.description)]
                    )
                    info_list.append(info_dict)
            return info_list
