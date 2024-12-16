from dataclasses import dataclass
from domain.order import Order, OrderLine
import logging
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from infrastructure.context.mysql_context_manager import MysqlContextManager
from typing import List

module_logger = logging.getLogger()



@dataclass
class OrderRepository:
    config: MysqlCMConfig
    config_dict: dict = None


    def __post_init__(self):
        self.config_dict = self.config.model_dump()

    
    def add_order(self, order_query:str):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Could not connect to a db")
            else:
                module_logger.info(order_query)
                cur.execute(order_query)
                module_logger.info(cur.lastrowid)
                return cur.lastrowid
            
    def add_order_lines(self, order_line_query_list: List[str]):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Could not connect to a db")
            else:
                for order_line_query in order_line_query_list:
                    module_logger.info(order_line_query)
                    cur.execute(order_line_query)
