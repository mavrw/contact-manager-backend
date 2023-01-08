from typing import List

from sqlalchemy.orm import Session

from Utils import hash_contact_photo
from database import SessionLocal, engine
from storage_provider.StorageProvider import StorageProvider
from storage_provider.mysql.models import DBContact, Base
from storage_provider.mysql.models import Schema


class MySQLProvider(StorageProvider):
    """ A  provider for MySQL storage """

    """ Init """

    def __init__(self):
        super().__init__()
        Base.metadata.create_all(bind=engine)
        self.set_schema(Schema.Contact)

    """ Override Methods """

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_schema(self):
        return self.schema

    def set_schema(self, rm):
        self.schema = rm

    def create_contact(self, db: Session, contact: Schema.Contact) -> DBContact:
        db_contact = DBContact(**contact.dict())
        contact_photo_hash = hash_contact_photo(str(db_contact.id))
        db_contact.contact_photo = contact_photo_hash
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    def update_contact(self, db: Session, contact_id: int, new_info: Schema.Contact) -> DBContact:
        contact = db.query(DBContact).get(contact_id)
        for key, value in new_info.dict().items():
            if value is not None:
                setattr(contact, key, value)
        db.commit()
        db.refresh(contact)
        return contact

    def delete_contact(self, db: Session, contact_id):
        if self.get_contact_by_id(db, contact_id) is not None:
            db.query(DBContact).filter(DBContact.id == contact_id).delete()
            db.commit()
            return True
        else:
            return False

    def get_all_contacts(self, db: Session, skip: int = 0, limit: int = 100) -> List[DBContact]:
        return db.query(DBContact).offset(skip).limit(limit).all()

    def get_contact_by_id(self, db: Session, contact_id: int) -> DBContact:
        return db.query(DBContact).filter(DBContact.id == contact_id).first()
