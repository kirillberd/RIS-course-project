from pydantic import BaseModel, Field
from typing import Optional

class UserQuery(BaseModel):
    role: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None



class OwnerBillboardsQuery(BaseModel):
   owner_id: int = Field(..., gt=0)
   city: Optional[str] = None
   min_quality: Optional[int] = Field(None, ge=1, le=5)