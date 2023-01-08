from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from storage_provider.mysql.MySQLStorageProvider import MySQLProvider

db_provider = MySQLProvider()

app = FastAPI()


@app.post("/contact/", response_model=db_provider.get_schema())
async def create_contact(contact: db_provider.get_schema(), db: Session = Depends(db_provider.get_db)):
    try:
        result_contact = db_provider.create_contact(db, contact)
        return result_contact
    except Exception as e:  # Using a catch-all for the time being. This is bad practice but whatever, loser.
        msg = str(e)
        raise HTTPException(status_code=400, detail=msg)


@app.get("/contact/all/", response_model=List[db_provider.get_schema()])
async def get_all_contacts(db: Session = Depends(db_provider.get_db)):
    return db_provider.get_all_contacts(db)


@app.get("/contact/{contact_id}/", response_model=db_provider.get_schema())
async def get_contact_by_id(contact_id: int, db: Session = Depends(db_provider.get_db)):
    try:
        contact = db_provider.get_contact_by_id(db, contact_id)
        if contact is not None:
            return contact
        else:
            raise KeyError
    except KeyError:
        msg = f"{contact_id} is not a known contact ID"
        raise HTTPException(status_code=404, detail=msg)


@app.delete("/contact/{contact_id}/")
async def delete_contact_by_id(contact_id: int, db: Session = Depends(db_provider.get_db)):

    try:
        if db_provider.delete_contact(db, contact_id):
            return {"message": f"Successfully deleted Contact with ID:{contact_id}"}
        else:
            raise KeyError
    except KeyError:
        msg = f"Unknown Contact ID: {contact_id}"
        raise HTTPException(status_code=404, detail=msg)


@app.put("/contact/{contact_id}/", response_model=db_provider.get_schema())
async def update_contact_by_id(contact_id: int, contact_info: db_provider.get_schema(),
                               db: Session = Depends(db_provider.get_db)):
    updated_contact = db_provider.update_contact(db, contact_id, contact_info)
    return updated_contact
