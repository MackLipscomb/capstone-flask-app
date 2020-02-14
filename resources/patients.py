from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

import models

patient = Blueprint('patient', 'patient')


@patient.route('/<id>', methods = ["GET"])
def get_one_patient(id):
    try:
        patient = models.Patient.get_by_id(id)
        patient_dict = model_to_dict(patient)
        return jsonify(data = patient_dict, status = {'code': 200, 'message': f'Found Patient with id {patient.id}'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error finding the patient'})


#update route
@patient.route('/<id>', methods=["PUT"])
def update_patient(id):
    try:
        payload = request.get_json()
        query = models.Patient.update(**payload).where(models.Patient.id == id)
        query.execute()
        updated_patient = model_to_dict(models.Patient.get_by_id(id))
        return jsonify(data = updated_patient, status = {'code': 200, 'message': 'Patient information updated'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'Update failed'})


@patients.route('/<id>', methods = ["DELETE"])
def delete_patient(id):
    try:
        patient = models.Patient.get_by_id(id)
        patient_dict = model_to_dict(patient)
        query = models.Patient.delete().where(models.Patient.id == id)
        query.execute()
        delete_symptoms = models.Health.delete().where(models.Health.symptoms == patient_dict['username'])
        delete_symptoms.execute()
        return jsonify(data = 'Patient and Symptoms successfully deleted', status = {'code': 200, 'message': 'Patient deleted'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'Failed to delete group from the database'})


