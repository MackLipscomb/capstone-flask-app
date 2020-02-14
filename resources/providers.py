from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict


import models

provider = Blueprint('provider', 'provider')



@provider.route('/<id>', methods = ["GET"])
def get_one_provider(id):
    try:
        providers = models.Provider.get_by_id(id)
        providers_dict = model_to_dict(providers)
        return jsonify(data = providers_dict, status = {'code': 200, 'message': f'Found providers with id {providers.id}'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error finding the provider'})


#create route
@provider.route('/<id>', methods = ["PUT"])
def update_provider(id):
    try:
        payload = request.get_json()
        query = models.Provider.update(**payload).where(models.Provider.id == id)
        query.execute()
        updated_provider = model_to_dict(models.Provider.get_by_id(id))
        return jsonify(data = updated_provider, status = {'code': 200, 'message': "Profile updated"})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error updating the provider profile'})


#delete route
@provider.route('/<id>', methods = ["DELETE"])
def delete_provider(id):
    try:
        query = models.Provider.delete().where(models.Provider.id == id)
        provider_delete = models.Health.delete()['diagnosis']
        provider_delete.execute()
        query.execute()
        return jsonify(data = 'issues successfully deleted', status = {'code': 200, 'message': 'Provider and diagnosis deleted'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error deleting the entries'})
