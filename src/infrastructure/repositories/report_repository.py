from dataclasses import dataclass
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from infrastructure.context.mysql_context_manager import MysqlContextManager
from typing import List
import logging

module_logger = logging.getLogger()

@dataclass
class ReportRepository:
    config: MysqlCMConfig
    config_dict: dict = None

    def __post_init__(self):
        self.config_dict = self.config.model_dump()


    def check_exists(self, query):
        ...

