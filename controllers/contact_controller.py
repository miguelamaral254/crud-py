from flask_restful import Resource, reqparse
from services.contact_service import ContactService

class ContactController(Resource):
    def __init__(self):
        self.contact_service = ContactService()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
        parser.add_argument('phone', type=str, required=True, help='Phone cannot be blank')
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
        args = parser.parse_args()

        contact, status_code = self.contact_service.create_contact(args['name'], args['phone'], args['email'])

        return contact, status_code

    def get(self, contact_id=None):
        if contact_id:
            contact = self.contact_service.get_contact_by_id(contact_id)
            if contact:
                return {'contact': contact}, 200
            else:
                return {'message': 'Contact not found'}, 404
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('page', type=int, default=1, help='Page number (default is 1)')
            parser.add_argument('page_size', type=int, default=10, help='Number of items per page (default is 10)')
            args = parser.parse_args()

            contacts_data = self.contact_service.get_all_contacts(page=args['page'], page_size=args['page_size'])
            return contacts_data, 200

    def put(self, contact_id):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', type=str, required=False)
        parser.add_argument('email', type=str, required=False)
        args = parser.parse_args()

        contact = self.contact_service.update_contact(contact_id, args)
        if contact:
            return {'message': 'Contact updated', 'contact': contact}, 200
        else:
            return {'message': 'Contact not found'}, 404

    def delete(self, contact_id):
        result = self.contact_service.delete_contact(contact_id)
        if result:
            return {'message': 'Contact deleted'}, 200
        else:
            return {'message': 'Contact not found'}, 404