class StorageProvider:

    schema: object

    def __init__(self):
        pass

    def get_db(self):
        """ Get database session """
        pass

    def get_schema(self):
        """ Returns the storage provider's schema """
        pass

    def set_schema(self, schema: object):
        """ Sets the schema of the provider """
        pass

    def create_contact(self, db, contact):
        """ Create a new contact in the database """
        pass

    def update_contact(self, db, contact_id, new_info):
        """ Update a contact in the database with new information """
        pass

    def delete_contact(self, db, contact_id):
        """ Delete a contact from the database via it's ID """
        pass

    def get_all_contacts(self, db):
        """ Gets all contacts from the database """
        pass

    def get_contact_by_id(self, db, contact_id):
        """ Gets contact from the database by contact_id """
        pass
