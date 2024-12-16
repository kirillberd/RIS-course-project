from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Order(BaseModel):
    registration_date: datetime
    total_cost: float
    tenant_id: Optional[int] = None
    id: Optional[int] = None

class OrderLine(BaseModel):
    date_begin: datetime
    date_end: datetime
    cost: float
    billboard_id: int
    id: Optional[int] = None
    order_id: Optional[int] = None
    