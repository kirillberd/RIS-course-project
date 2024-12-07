from dataclasses import dataclass
from infrastructure.configs.mysql_cm_config import MysqlCMConfig
from domain.user import BaseUser, Customer, BillboardOwner, Analyst
from infrastructure.context.mysql_context_manager import MysqlContextManager
import logging
from typing import List

module_logger = logging.getLogger(__name__)
@dataclass
class UserRepository:
    config: MysqlCMConfig
    config_dict: dict = None

    def __post_init__(self):
        self.config_dict = self.config.model_dump()


    def add(self,query: str):
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Could not connect to a database.")
            else:
                result = cur.execute(query)
                module_logger.info(result)
        
    def get_one(self, query: str) -> BaseUser:
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
                
    def get_many(self, query: str) -> List[BaseUser]:
        with MysqlContextManager(self.config_dict) as cur:
            if cur is None:
                raise Exception("Could not connect to a database")
            else:
                cur.execute(query)
                result = cur.fetchall()
                module_logger.info(result)
                user_list: List[BaseUser] = []
                for user in result:
                    res_dict =  dict([(item[0], user[i]) for i, item in enumerate(cur.description)])
                    role = res_dict["role"]
                    module_logger.info(res_dict)
                    if role == "customer":
                        user_list.append(Customer.model_validate(res_dict))
                    elif role == "owner":
                        user_list.append(BillboardOwner.model_validate(res_dict))
                    elif role == "analyst":
                        user_list.append(Analyst.model_validate(res_dict))
                    else:
                        raise Exception("Unknown user_role")
                return user_list
            
            