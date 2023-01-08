from Models import DBContact, Contact


class StorageProviderInterface:

    def create_contact(self, contact: Contact) -> DBContact:
        """ Create a new contact in the database """
        pass

    def update_contact(self, contact_id, new_info: Contact) -> DBContact:
        """ Update a contact in the database with new information """
        pass

    def delete_contact(self, contact_id):
        """ Delete a contact from the database via it's ID """
        pass

    def get_all_contacts(self) -> dict[int, DBContact]:
        """ Gets all contacts from the database """
        pass

    def get_contact_by_id(self, contact_id: int) -> DBContact:
        """ Gets contact from the database by contact_id """
        pass
