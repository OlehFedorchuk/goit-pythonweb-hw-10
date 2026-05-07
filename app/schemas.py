from pydantic import BaseModel

class ContactSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: str
    additional_data: str
class ContactCreate(ContactSchema):
    pass

class ContactResponse(ContactSchema):
    id: int

    class Config:
        from_attributes = True