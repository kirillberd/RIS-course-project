from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Billboard(BaseModel):
    id: Optional[int]
    cost: float
    size: float
    installation_date: Optional[datetime]
    addres: str
    quality_indicator: int
    city: str
    direction: str
    billboard_owner_id: Optional[int]


class BillboardOwner(BaseModel):
    id: int
    last_name: str
    birthdate: datetime
    addres: str
    phone_number: str = Field(pattern=r"^(?:\+7|8)?\s?\(?\d{3}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}$")


class BillboardTenant(BaseModel):
    id: Optional[int]
    last_name: str
    addres: str
    contract_date: datetime
    phone_number: str = Field(Field(pattern=r"^(?:\+7|8)?\s?\(?\d{3}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}$"))


class Order(BaseModel):
    id: Optional[int]
    registration_date: datetime
    total_cost: float
    tenant_id: Optional[int]

class OrderLine(BaseModel):
    id: Optional[int]
    date_begin: datetime
    date_end: datetime
    cost: float
    order_id: int
    billboard_id: int
    
