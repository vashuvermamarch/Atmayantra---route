from pydantic import BaseModel, EmailStr

class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone_no: str
    message: str

class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True   # 👈 instead of orm_mode = True
