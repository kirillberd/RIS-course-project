from pydantic import BaseModel
from typing import Optional

class UserQuery(BaseModel):
    role: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None