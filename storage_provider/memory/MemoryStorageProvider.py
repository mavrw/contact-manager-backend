from storage_provider.memory.models import Contact, DBContact
from storage_provider.StorageProvider import StorageProvider
from Utils import hash_contact_photo

next_available_contact_id: int = 1


class MemoryStorageProvider(StorageProvider):
    """ A provider for In-memory storage """

    contacts: dict[int, DBContact]
    next_available_contact_id: int

    """ Init """

    def __init__(self):
        self.contacts = {}
        self.next_available_contact_id = 1

    """ Implementation Specific Methods """

    def get_next_available_contact_id(self):
        next_id = self.next_available_contact_id
        self.next_available_contact_id += 1
        return next_id

    """ Override Methods """

    def create_contact(self, contact: Contact) -> DBContact:
        contact_id = self.get_next_available_contact_id()
        saved_contact = DBContact(**contact.dict(),
                                  id=contact_id,
                                  contact_photo=hash_contact_photo(str(contact_id))
                                  )
        self.contacts.update({saved_contact.id: saved_contact})
        print(f"Saved contact with ID:{saved_contact.id}")

        return saved_contact

    def update_contact(self, contact_id, new_info: Contact) -> DBContact:
        contact_dict = self.contacts.get(contact_id).dict()
        contact_dict.update(**new_info.dict())
        saved_contact = DBContact(**contact_dict)
        saved_contact.contact_photo = hash_contact_photo(str(saved_contact.id))
        self.contacts.update({saved_contact.id: saved_contact})
        print(f"Updated contact with ID:{saved_contact.id}")

        return saved_contact

    def delete_contact(self, contact_id: int):
        self.contacts.pop(contact_id)

    def get_all_contacts(self) -> dict[int, DBContact]:
        return self.contacts

    def get_contact_by_id(self, contact_id: int) -> DBContact:
        return self.contacts.get(contact_id)
