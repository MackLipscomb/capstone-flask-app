from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required

import models

patients = Blueprint('patients', 'patients')

#register, login, logout
@patients.route('/register', methods = ["POST"])
def register():
    payload = request.get_json()
    payload['email'].lower()
    try:
        models.Patient.get(models.Patient.email == payload['email'])
        return jsonify(data = {}, status = {'code': 400, 'message': 'A Patient with that email already exists'})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        patient = models.Patient.create(**payload)
        login_user(patient)
        patient_dict = model_to_dict(patient)
        del patient_dict['password']
        return jsonify(data = patient_dict, status = {'code': 200, 'message': 'Patient succesfully registered'})


@patients.route('/login', methods = ["POST"])
def login():
    payload = request.get_json()
    payload['email'].lower()
    try:
        patient = models.Patient.get(models.Patient.email == payload['email'])
        patient_dict = model_to_dict(patient)
        if(check_password_hash(patient_dict['password'], payload['password'])):
            del patient_dict['password']
            login_user(patient)
            return jsonify(data = patient_dict, status = {'code': 200, 'message': "Login successfull"})
        else:
            return jsonify(data = {}, status = {'code': 400, 'message': 'Email or password is incorrect'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'Email or password is incorrect'})       

@patients.route('/logout', methods = ["GET"])
def logout():
    name = model_to_dict(current_user)['name']
    logout_user()
    return jsonify(data = {}, status = {'code': 200, 'message': f'{name} has logged out'}) 


#show route...access a specific patient's account upon login
@patients.route('/<id>', methods = ["GET"])
@login_required
def get_one_patient(id):
    try:
        patient = models.Patient.get_by_id(id)
        patient_dict = model_to_dict(patient)
        return jsonify(data = patient_dict, status = {'code': 200, 'message': f'Found Patient with id {patient.id}'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error finding the patient'})


#create route for symptoms/health issues
@patients.route('/', methods = ["POST"])
@login_required
def create_symptoms():
    try:
        payload = request.get_json()
        payload['symptoms'] = current_user.id
        patient = models.Patient.create(**payload)
        patient_dict = model_to_dict(patient)
        return jsonify(data = patient_dict, status = {'code': 200, 'message': "Symptomes added"})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error updating patient symptoms'})


#delete route for deleting health issues
@patients.route('/<id>', methods = ["DELETE"])
def delete_symptoms(id):
    try:
        query = models.Patient.delete()['symptoms'].where(models.Patient.id == id)
        query.execute()
        return jsonify(data = 'issues successfully deleted', status = {'code': 200, 'message': 'Issues successfully deleted'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error deleting the issues'})



