from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Billboard(BaseModel):
    id: Optional[int]
    cost: float
    size: float
    addres: str
    quality_indicator: int
    city: str
    direction: str
    billboard_owner_id: Optional[int] = None
    installation_date: Optional[datetime] = None


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
    

class BillboardQuery(BaseModel):
    city: Optional[str] = None
    direction: Optional[str] = None
    cost_min: Optional[float] = None
    cost_max: Optional[float] = None
    size_min: Optional[float] = None
    size_max: Optional[float] = None
    min_quality: Optional[int] = None
    address: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
