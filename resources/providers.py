from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user

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
