class StorageProvider:

    def __init__(self):
        pass

    def create_contact(self, contact):
        """ Create a new contact in the database """
        pass

    def update_contact(self, contact_id, new_info):
        """ Update a contact in the database with new information """
        pass

    def delete_contact(self, contact_id):
        """ Delete a contact from the database via it's ID """
        pass

    def get_all_contacts(self):
        """ Gets all contacts from the database """
        pass

    def get_contact_by_id(self, contact_id):
        """ Gets contact from the database by contact_id """
        pass
