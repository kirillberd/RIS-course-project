from dataclasses import dataclass
from domain.billboards import Billboard
import logging
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from infrastructure.context.mysql_context_manager import MysqlContextManager

logger = logging.getLogger(__name__)

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
                logger.info(billboard)