from pydantic import BaseModel, Field
from typing import Optional

class BaseUser(BaseModel):
    password: str
    username: str
    firstname: str
    lastname: str
    phone: str
    role: str
    id: Optional[int] = None


class Customer(BaseUser):
    role: str = Field(default="customer")


class BillboardOwner(BaseUser):
    role: str = Field(default="owner")

class Analyst(BaseUser):
    role: str = Field(default="analyst")

class UserLogin(BaseModel):
    username: str
    password: str

