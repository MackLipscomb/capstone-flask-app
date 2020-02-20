import os
from flask import Flask, jsonify, g, request
from playhouse.shortcuts import model_to_dict
from flask_login import LoginManager
from flask_cors import CORS
app = Flask(__name__)


import models

from resources.patients import patient
from resources.providers import provider
from resources.health import health




CORS(patient, origin=['http://localhost:3000'], supports_credentials = True)
CORS(provider, origin=['http://localhost:3000'], supports_credentials = True)
CORS(health, origin=['http://localhost:3000'], supports_credentials = True)
CORS(app, origin=['http://localhost:3000'], supports_credentials = True)



app.register_blueprint(patient, url_prefix='/api/v1/patients')
app.register_blueprint(provider, url_prefix='/api/v1/providers')
app.register_blueprint(health, url_prefix='/api/v1/health')


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


@app.route('/register', methods=["POST"])
def register():
    print("line 48")
    payload = request.get_json()
    
    if payload['type'] == 'Patient':
        try:
            models.Patient.get(models.Patient.email == payload['email'] or
            models.Patient.username == payload['username'])
            return jsonify(data = {}, status = {'code': 400, 'message': 'A user with that email already exists'})
        except models.DoesNotExist:
            del payload['type']
            del payload['specialty']
            patient = models.Patient.create(**payload)
            idOfPatient = patient.id
            patient_dict = model_to_dict(patient)
            return jsonify(data = patient_dict, status = {'code': 200, 'message': 'Patient id created'})
    elif payload['type'] == 'Provider':
        try:
            models.Provider.get(models.Provider.email == payload['email'] or 
            models.Provider.username == payload['username'])
            return jsonify(data = {}, status = {'code': 400, 'message': 'A provider with that email already exists'})
        except models.DoesNotExist:
            del payload['type']
            provider = models.Provider.create(**payload)
            idOfProvider = provider.id

            #add in function to request provider DEA number for verification ? link to models
            return jsonify(data = {}, status = {'code': 200, 'message': 'Provider registered'})


@app.route('/login', methods = ["POST"])
def login():
    payload = request.get_json()
    print(payload)
    if payload['type'] == 'Patient':
        try:
            patient = models.Patient.get(models.Patient.email == payload['email'])
            patientdict = model_to_dict(patient)
            if(patientdict['password'] == payload['password']):
                del patientdict['password']
                idofPatient = patientdict['id']
                patientdict['type'] = payload['type']
                return jsonify(data = patientdict, status = {'code': 200, 'message': 'Login successfull'})

            else:
                return jsonify(data = {}, status = {'code': 400, 'message': 'Email or password is incorrect'})
        except models.DoesNotExist:
            return jsonify(data = {}, status = {'code': 400, 'message': 'Email or password is incorrect'})
    
    elif payload['type'] == 'Provider':
        try:
            provider = models.Provider.get(models.Provider.email == payload['email'])
            providerdict = model_to_dict(provider)
            if(providerdict['password'] == payload['password']):
                del providerdict['password']
                idOfProvider = providerdict['id']
                # providerdict['type'] == payload['type']
                return jsonify(data = {}, status = {'code': 200, 'message': 'Login Successfull'})
            else:
                return jsonify(data = {}, status = {'code': 400, 'message': 'Email or Password is incorrect'})
        except models.DoesNotExist:
            return jsonify(data = {}, status = {'code': 400, 'message': 'Email or Password is incorrect'})

@app.route('/logout', methods = ['GET'])
def logout():
    logout_user
    return jsonify(data = {}, status = {'code': 200, 'message': 'Please login again'})



DEBUG = True
PORT = 8000
if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)