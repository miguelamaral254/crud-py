from flask_restful import Resource, reqparse
from services.contact_service import ContactService

class ContactController(Resource):
    def __init__(self):
        self.contact_service = ContactService()

    # Criar novo contato
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
        parser.add_argument('phone', type=str, required=True, help='Phone cannot be blank')
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
        args = parser.parse_args()

        # Chama o service para salvar o contato
        contact = self.contact_service.create_contact(args['name'], args['phone'], args['email'])
        return {'message': 'Contact created', 'contact': contact}, 201

    # Buscar contato por nome
    def get(self, name=None):
        if name:
            contact = self.contact_service.get_contact_by_name(name)
            if contact:
                return {'contact': contact}, 200
            else:
                return {'message': 'Contact not found'}, 404
        else:
            contacts = self.contact_service.get_all_contacts()
            return {'contacts': contacts}, 200

    # Atualizar contato
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', type=str, required=False)
        parser.add_argument('email', type=str, required=False)
        args = parser.parse_args()

        contact = self.contact_service.update_contact(name, args)
        if contact:
            return {'message': 'Contact updated', 'contact': contact}, 200
        else:
            return {'message': 'Contact not found'}, 404

    # Deletar contato
    def delete(self, name):
        result = self.contact_service.delete_contact(name)
        if result:
            return {'message': 'Contact deleted'}, 200
        else:
            return {'message': 'Contact not found'}, 404