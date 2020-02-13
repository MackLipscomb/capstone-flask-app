from flask import Flask, jsonify, g
from flask_login import LoginManager
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = 'mysecretkey'
login_manager = LoginManager()
login_manager.init_app(app)

import models

from resources.patients import patients
from resources.providers import providers

@login_manager.user_loader
def load_user(userid):
    try:
        return models.Patient.get(models.Patient.id == userid) or models.Provider.get(models.Provider.id == userid)
    except models.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def notauthorized():
    return jsonify(data = {'error': 'Not logged in'}, status = {'code': 400, 'message': 'You must be logged in to access the site'})


CORS(patients, origin=['http://localhost:3000/patients'], supports_credentials = True)
CORS(providers, origin=['http://localhost:3000/providers'], supports_credentials = True)


app.register_blueprint(patients, url_prefix='/api/v1/patients')
app.register_blueprint(providers, url_prefix='/api/v1/providers')


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    return 'welcome'


# @app.route('/register', methods=["POST"])
# def register():
#     payload = request.get_json()
#     if payload['type'] == 'Patient':
#         try:
#             models.Patient.get(models.Patient.email == payload['email'])
#             return jsonify(data = {}, status = {'code': 400, 'message': 'A user with that email already exists'})
#         except models.DoesNotExist:
#             del payload['type']
#             patient = models.Payload.create(**payload)
#             idOfPatient = patient.id
#             return jsonify(data = {}, status = {'code': 200, 'message': 'Patient id created'})
#     elif payload['type'] == 'Provider':
#         try:
#             models.Provider.get(models.Provider.email == payload['email'])
#             return jsonify(data = {}, status = {'code': 400, 'message': 'A provider with that email already exists'})
#         except models.DoesNotExist:
#             del payload['type']
#             provider = models.Provider.create(**payload)
#             idOfProvider = provider.id

#             #add in function to request provider DEA number for verification ? link to models

#             return jsonify(data = {}, status = {'code': 200, 'message': 'Provider registered'})


# @app.route('/login', methods = ["POST"])
# def login():
#     payload = request.get_json()
#     if payload['type'] == 'Provider'
    









DEBUG = True
PORT = 8000
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)