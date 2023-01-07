import hashlib

from fastapi import FastAPI, HTTPException, status

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


app = FastAPI()

global next_available_contact_id
global contacts


next_available_contact_id = 1

contacts = {}


def get_next_available_contact_id():

    next_id = next_available_contact_id
    next_available_contact_id += 1
    return next_id


def hash_contact_photo(s: str):
    photo_hash = hashlib.md5(s.encode())
    return photo_hash.hexdigest()


def save_contact(contact: Contact):
    contact_id = get_next_available_contact_id()
    saved_contact = DBContact(**contact.dict(),
                              id=contact_id,
                              contact_photo=hash_contact_photo(str(contact_id))
                              )
    contacts.update({saved_contact.id: saved_contact})
    print(f"Saved contact with ID:{saved_contact.id}")
    return saved_contact


def update_contact(contact_id, new_info: Contact):
    contact_dict = contacts.get(contact_id).dict()
    contact_dict.update(**new_info.dict())
    saved_contact = DBContact(**contact_dict)
    saved_contact.contact_photo = hash_contact_photo(str(saved_contact.id))
    contacts.update({saved_contact.id: saved_contact})
    print(f"Updated contact with ID:{saved_contact.id}")
    return saved_contact


@app.post("/contact/")
async def create_contact(contact: Contact):
    try:
        result_contact = save_contact(contact)
        return result_contact
    except: # Using a catch-all for the time being. This is bad practice but whatever, loser.
        msg = "Error while creating contact. Ensure you are providing a valid request."
        raise HTTPException(status_code=400, detail=msg)


@app.get("/contact/all/")
async def get_all_contacts():
    return contacts


@app.get("/contact/{contact_id}/")
async def get_contact_by_id(contact_id: int):
    try:
        return contacts.get(contact_id)
    except KeyError:
        msg = f"{contact_id} is not a known contact ID"
        raise HTTPException(status_code=404, detail=msg)


@app.delete("/contact/{contact_id}/")
async def delete_contact_by_id(contact_id: int):
    try:
        contacts.pop(contact_id)
        return {"message": f"Successfully deleted Contact with ID:{contact_id}"}
    except KeyError:
        msg = f"Unknown Contact ID: {contact_id}"
        raise HTTPException(status_code=404, detail=msg)


@app.put("/contact/{contact_id}/")
async def update_contact_by_id(contact_id: int, contact_info: Contact):
    updated_contact = update_contact(contact_id, contact_info)
    return updated_contact
