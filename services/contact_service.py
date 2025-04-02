from models.contact_model import Contact
from utils.db import get_db

class ContactService:
    def __init__(self):
        self.db = get_db()

    def create_contact(self, name, phone, email):
        contact = Contact(name, phone, email)
        self.db['contacts'].insert_one(contact.to_dict())
        return contact.to_dict()

    def get_contact_by_name(self, name):
        contact = self.db['contacts'].find_one({"name": name})
        if contact:
            return contact
        return None

    def get_all_contacts(self):
        contacts = []
        for contact in self.db['contacts'].find():
            contacts.append(contact)
        return contacts

    def update_contact(self, name, updated_data):
        query = {"name": name}
        update_fields = {}

        if updated_data.get('phone'):
            update_fields["phone"] = updated_data['phone']
        if updated_data.get('email'):
            update_fields["email"] = updated_data['email']

        if update_fields:
            self.db['contacts'].update_one(query, {"$set": update_fields})
            return self.get_contact_by_name(name)
        return None

    def delete_contact(self, name):
        result = self.db['contacts'].delete_one({"name": name})
        return result.deleted_count > 0