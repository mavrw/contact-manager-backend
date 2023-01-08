from typing import Union

from pydantic import BaseModel


class Contact(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    phone_number: Union[str, None] = None
    email: Union[str, None] = None


class DBContact(BaseModel):
    id: int
    first_name: str
    last_name: Union[str, None] = None
    phone_number: Union[str, None] = None
    email: Union[str, None] = None
    contact_photo: str


class Schema:
    class Contact(DBContact):

        class Config:
            orm_mode = True
