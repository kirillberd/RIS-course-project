from pydantic import BaseModel


class BaseUser(BaseModel):
    id: int
    email: int
    password: int
    username: int


class Customer(BaseUser):
    role = "customer"


class BillboardOwner(BaseUser):
    role = "billboard-owner"

class Analyst(BaseUser):
    role = "analyst"

    

