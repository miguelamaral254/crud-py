from models.contact_model import Contact
from utils.db import get_db
from bson import ObjectId

class ContactService:
    def __init__(self):
        self.db = get_db()

    def create_contact(self, name, phone, email):
        try:
            # Verificar se o email já existe
            existing_contact = self.db['contacts'].find_one({"email": email})
            if existing_contact:
                # Retornar um erro mais claro
                return {"message": "Email already in use", "error": "Email conflict"}, 409

            contact = Contact(name, phone, email)
            self.db['contacts'].insert_one(contact.to_dict())
            return {"message": "Contact created", "contact": contact.to_dict()}, 201

        except Exception as e:
            print(f"Erro ao criar o contato: {e}")
            return {"error": "An error occurred while creating the contact"}, 500

    def get_contact_by_id(self, contact_id):
        try:
            contact = self.db['contacts'].find_one({"_id": ObjectId(contact_id)})
            if contact:
                contact['_id'] = str(contact['_id'])
                return contact
        except Exception as e:
            print(f"Erro ao buscar o contato por ID: {e}")
        return None

    def get_all_contacts(self, page=1, page_size=10):
        contacts = []
        skip = (page - 1) * page_size
        limit = page_size

        for contact in self.db['contacts'].find().skip(skip).limit(limit):
            contact['_id'] = str(contact['_id'])
            contacts.append(contact)

        total_contacts = self.db['contacts'].count_documents({})
        total_pages = (total_contacts + page_size - 1) // page_size

        return {
            'contacts': contacts,
            'page': page,
            'page_size': page_size,
            'total_contacts': total_contacts,
            'total_pages': total_pages
        }

    def update_contact(self, contact_id, updated_data):
        try:
            contact = self.get_contact_by_id(contact_id)
            if not contact:
                return {"error": "Contact not found"}

            # Se o email está sendo atualizado, verificar se o novo email já existe
            if updated_data.get('email'):
                existing_contact = self.db['contacts'].find_one({"email": updated_data['email']})
                if existing_contact:
                    return {"error": "Email already in use"}

            update_fields = {}
            if updated_data.get('phone'):
                update_fields["phone"] = updated_data['phone']
            if updated_data.get('email'):
                update_fields["email"] = updated_data['email']

            if update_fields:
                self.db['contacts'].update_one({"_id": ObjectId(contact_id)}, {"$set": update_fields})
                return self.get_contact_by_id(contact_id)

        except Exception as e:
            print(f"Erro ao atualizar o contato: {e}")
            return {"error": "An error occurred while updating the contact"}

        return None

    def delete_contact(self, contact_id):
        try:
            contact = self.get_contact_by_id(contact_id)
            if contact:
                result = self.db['contacts'].delete_one({"_id": ObjectId(contact_id)})
                return result.deleted_count > 0
            return False
        except Exception as e:
            print(f"Erro ao deletar o contato: {e}")
            return {"error": "An error occurred while deleting the contact"}