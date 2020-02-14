from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

import models

health = Blueprint('health', 'health')


@health.route('/', methods=["GET"])
def all_issues():
    try:
        issue = [model_to_dict(issue) for issue in models.Health.select()]
        return jsonify(data = issue, status = {'code': 200, 'message': 'Found the issue'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'Error finding the issues'})


@health.route('/', methods=["POST"])
def create_issue():
    try:
        payload = request.get_json()
        issue = models.Health.create(**payload)
        issue_dict = model_to_dict(issue)
        return jsonify(data = {}, status = {'code': 200, 'message': 'Issue added'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error creating the issue'})


@health.route('/<id>', methods=["GET"])
def get_one_issue(id):
    try:
        issue = models.Health.get_by_id(id)
        issue_dict = model_to_dict(issue)
        return jsonify(data = issue_dict, status = {'code': 200, 'message': f'Found the issue by id: {issue.id}'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error finding the issue'})


@health.route('/<id>', methods=["PUT"])
def update_issue(id):
    try:
        payload = request.get_json()
        query = models.Health.update(**payload).where(models.Health.id == id)
        query.execute()
        updated_issue = model_to_dict(models.Health.get_by_id(id))
        return jsonify(data = updated_issue, status = {'code': 200, 'message': 'Information updated successfully'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'error updating the issue'})

@health.route('/<id>', methods=["DELETE"])
def delete_issue(id):
    try:
        query = models.Health.delete().where(models.Health.id == id)
        query.execute()
        return jsonify(data = 'issue successfully deleted', status = {'code': 200, 'message': 'Issues successfully deleted'})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {'code': 400, 'message': 'Failed to delete the issue'})


