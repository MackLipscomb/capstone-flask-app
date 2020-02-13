from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required

import models

providers = Blueprint('providers', 'providers')


@providers.route('/register', methods = ["POST"])
def register():
    payload = request.get_json()
    payload['email'].lower()
    try:
        models.Provider.get(models.Provider.email == payload['email'])
        return jsonify(data = {}, status = {'code': 400, 'message': 'A provider with that email already exists'})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        provider = models.Provider.create(**payload)
        login_user(provider)
        provider_dict = model_to_dict(provider)
        del provider_dict['password']
        return jsonify(data = provider_dict, status = {'code': 200, 'message': 'provider succesfully registered'})


@providers.route('/login', methods = ["POST"])
def login():
    payload = request.get_json()
    payload['email'].lower()
    try:
        provider = models.Provider.get(models.Provider.email == payload['email'])
        provider_dict = model_to_dict(provider)
        if(check_password_hash(provider_dict['password'], payload['password'])):
            del provider_dict['password']
            login_user(provider)
            return jsonify(data = provider_dict, status = {'code': 200, 'message': "Login successfull"})
        else:
            return jsonify(data = {}, status = {'code': 400, 'message': 'Email or password is incorrect'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'Email or password is incorrect'})       

@providers.route('/logout', methods = ["GET"])
def logout():
    name = model_to_dict(current_user)['name']
    logout_user()
    return jsonify(data = {}, status = {'code': 200, 'message': f'{name} has logged out'}) 


#index route to show all provider's active patients
@providers.route('/', methods = ["GET"])
@login_required
def get_all_patients():
    try:
        patients = [model_to_dict(patient) for patient in models.Patient.select().where(models.Patient.symptoms_id == current_user.id)]
        for patient in patients:
            patient['diagnoses'].pop('password')
        return jsonify(data = patients, status = {'code': 200, 'message': 'Success finding the patients'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'Error getting the patients'})



#show route...access a specific providers's account upon login
@providers.route('/<id>', methods = ["GET"])
@login_required
def get_one_provider(id):
    try:
        providers = models.Providers.get_by_id(id)
        providers_dict = model_to_dict(providers)
        return jsonify(data = providers_dict, status = {'code': 200, 'message': f'Found providers with id {providers.id}'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error finding the providers'})


#create route for symptoms/health issues
@providers.route('/', methods = ["POST"])
@login_required
def create_diagnosis():
    try:
        payload = request.get_json()
        payload['diagnoses'] = current_user.id
        providers = models.Providers.create(**payload)
        providers_dict = model_to_dict(providers)
        return jsonify(data = providers_dict, status = {'code': 200, 'message': "Diagnosis added"})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error updatingproviders symptoms'})


#delete route for deleting health issues
@providers.route('/<id>', methods = ["DELETE"])
def delete_diagnosis(id):
    try:
        query = models.Providers.delete()['diagnoses'].where(models.Providers.id == id)
        query.execute()
        return jsonify(data = 'issues successfully deleted', status = {'code': 200, 'message': 'Issues successfully deleted'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error deleting the issues'})
