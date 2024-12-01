from dataclasses import dataclass
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from domain.user import BaseUser
from infrastructure.context.mysql_context_manager import MysqlContextManager
import logging

module_logger = logging.getLogger(__name__)
@dataclass
class UserRepository:
    config: MysqlCMConfig
    config_dict: dict = None

    def __post_init__(self):
        self.config_dict = self.config.model_dump()


    def add(self, user: BaseUser, query: str):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Test")
            else:
                result = cur.execute(query)
                module_logger.info(result)
        
    