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
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Could not conenct to a db")
            else:
                result = cur.execute(query)
                module_logger.info(result)
                return result
    def create_report(self, procedure_name, year, month):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Could not conenct to a db")
            else:
                cur.callproc(procedure_name, (year, month))

    def get_report(self, query):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Could not conenct to a db")
            else:
                cur.execute(query)
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                result = []
                for row in rows:
                    row_dict = {}
                    for i, value in enumerate(row):
                        row_dict[columns[i]] = value
                    result.append(row_dict)
                module_logger.info(result)
                return result