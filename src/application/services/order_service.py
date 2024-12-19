from dataclasses import dataclass
from domain.order import Order, OrderLine
import logging
from infrastructure.providers.sql_provider import SQLProvider
from infrastructure.repositories.order_repository import OrderRepository
from typing import List

module_logger = logging.getLogger(__name__)

@dataclass
class OrderService:
    order_repository: OrderRepository
    sql_provider: SQLProvider


    def make_order(self, order: Order, order_line_list: List[OrderLine]):
        order_query = self.sql_provider.get("create_order.sql", **order.model_dump())
        order_line_query_list = []
        order_id = int(self.order_repository.add_order(order_query))
        for order_line in order_line_list:
            order_line.order_id = order_id
            order_line_query = self.sql_provider.get("create_order_line.sql", **order_line.model_dump())
            order_line_query_list.append(order_line_query)

        self.order_repository.add_order_lines(order_line_query_list)
        return order_id