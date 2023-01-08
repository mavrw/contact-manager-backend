from fastapi import FastAPI, HTTPException

from storage_provider.memory.MemoryStorageProvider import MemoryStorageProvider
from storage_provider.memory.models import Contact


db_provider = MemoryStorageProvider()

app = FastAPI()


@app.post("/contact/")
async def create_contact(contact: Contact):
    try:
        result_contact = db_provider.create_contact(contact)
        return result_contact
    except:  # Using a catch-all for the time being. This is bad practice but whatever, loser.
        msg = "Error while creating contact. Ensure you are providing a valid request."
        raise HTTPException(status_code=400, detail=msg)


@app.get("/contact/all/")
async def get_all_contacts():
    return db_provider.get_all_contacts()


@app.get("/contact/{contact_id}/")
async def get_contact_by_id(contact_id: int):
    try:
        contact = db_provider.get_contact_by_id(contact_id)
        if contact:
            return contact
        else:
            raise KeyError
    except KeyError:
        msg = f"{contact_id} is not a known contact ID"
        raise HTTPException(status_code=404, detail=msg)


@app.delete("/contact/{contact_id}/")
async def delete_contact_by_id(contact_id: int):
    try:
        db_provider.delete_contact(contact_id)
        return {"message": f"Successfully deleted Contact with ID:{contact_id}"}
    except KeyError:
        msg = f"Unknown Contact ID: {contact_id}"
        raise HTTPException(status_code=404, detail=msg)


@app.put("/contact/{contact_id}/")
async def update_contact_by_id(contact_id: int, contact_info: Contact):
    updated_contact = db_provider.update_contact(contact_id, contact_info)
    return updated_contact
