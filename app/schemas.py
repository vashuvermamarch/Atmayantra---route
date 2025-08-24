from typing import Optional, Any
from pydantic import BaseModel, EmailStr, ConfigDict

class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone_no: str
    message: str

class ContactResponse(ContactBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ✅ Generic response wrapper
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
