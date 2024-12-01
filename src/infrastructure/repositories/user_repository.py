from dataclasses import dataclass
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from domain.user import BaseUser, Customer, BillboardOwner, Analyst
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
                raise Exception("Could not connect to a database.")
            else:
                result = cur.execute(query)
                module_logger.info(result)
        
    def get(self, query: str):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Could not connect to a database.")
            else:
                cur.execute(query)
                result = cur.fetchone()
                res_dict = dict([(item[0], result[i]) for i, item in enumerate(cur.description)])
                role = res_dict["role"]
                if role == "customer":
                    return Customer.model_validate(res_dict)
                elif role == "owner":
                    return BillboardOwner.model_validate(res_dict)
                elif role == "analyst":
                    return Analyst.model_validate(res_dict)
                else:
                    raise Exception("Unknown user role")
                
