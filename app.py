from flask import Flask
from flask_restful import Api
from controllers.contact_controller import ContactController

app = Flask(__name__)
api = Api(app)

# Definindo os endpoints da API
api.add_resource(ContactController, '/contacts', '/contacts/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)