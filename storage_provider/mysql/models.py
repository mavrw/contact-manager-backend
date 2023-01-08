from typing import Union

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from database import Base

""" Database Models (formerly models.py) """


class DBContact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    email = Column(String(255))
    contact_photo = Column(String(255))


""" Pydantic Models (formerly schema.py) """


class Schema:
    class Contact(BaseModel):
        id: Union[int, None] = None
        first_name: str
        last_name: Union[str, None] = None
        phone_number: Union[str, None] = None
        email: Union[str, None] = None
        contact_photo: Union[str, None] = None

        class Config:
            orm_mode = True
