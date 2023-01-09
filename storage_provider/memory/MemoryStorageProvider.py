from typing import List

from Utils import hash_contact_photo
from storage_provider.StorageProvider import StorageProvider
from storage_provider.memory.models import Contact, DBContact, Schema

next_available_contact_id: int = 1


class MemoryStorageProvider(StorageProvider):
    """ A provider for In-memory storage """

    contacts: dict[int, DBContact]
    next_available_contact_id: int

    """ Init """

    def __init__(self):
        super().__init__()
        self.contacts = {}
        self.next_available_contact_id = 1
        self.set_schema(Schema.Contact)

    """ Implementation Specific Methods """

    def get_next_available_contact_id(self):
        next_id = self.next_available_contact_id
        self.next_available_contact_id += 1
        return next_id

    """ Override Methods """

    def get_schema(self):
        return self.schema

    def set_schema(self, rm):
        self.schema = rm

    def create_contact(self, db, contact: Contact) -> DBContact:
        contact_id = self.get_next_available_contact_id()
        saved_contact = DBContact(**contact.dict(),
                                  id=contact_id,
                                  contact_photo=hash_contact_photo(str(contact_id))
                                  )
        self.contacts.update({saved_contact.id: saved_contact})
        print(f"Saved contact with ID:{saved_contact.id}")

        return saved_contact

    def update_contact(self, db, contact_id, new_info: Contact) -> DBContact:
        contact_dict = self.contacts.get(contact_id).dict()
        contact_dict.update(**new_info.dict())
        saved_contact = DBContact(**contact_dict)
        saved_contact.contact_photo = hash_contact_photo(str(saved_contact.id))
        self.contacts.update({saved_contact.id: saved_contact})
        print(f"Updated contact with ID:{saved_contact.id}")

        return saved_contact

    def delete_contact(self, db, contact_id: int) -> bool:
        try:
            self.contacts.pop(contact_id)
            return True
        except KeyError:
            return False

    def get_all_contacts(self, db) -> List[DBContact]:
        return list(self.contacts.values())

    def get_contact_by_id(self, db, contact_id: int) -> DBContact:
        return self.contacts.get(contact_id)
