from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Order(BaseModel):
    id: Optional[int]
    registration_date: datetime
    total_cost: float
    tenant_id: Optional[int] = None

class OrderLine(BaseModel):
    date_begin: datetime
    date_end: datetime
    cost: float
    order_id: int
    billboard_id: int
    id: Optional[int] = None
    