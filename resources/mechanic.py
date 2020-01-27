from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

mechanic = Blueprint('mechanic', 'mechanic')

# Index route
@mechanic.route('/', methods=["GET"])
# @login_required
def get_all_mechanic():
    try:
        mechanic = [model_to_dict(mechanic) for mechanic in models.Mechanic.select()]
        print(mechanic)
        for mechanic in mechanic:
            mechanic.pop('password')
        return jsonify(data=mechanic, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting the resources"})

# Create route
@mechanic.route('/', methods=["POST"])
# @login_required
def create_mechanic():
    try:
        payload = request.get_json()
        print(payload)
        # payload['owner'] = current_user.id
        mechanic = models.Mechanic.create(**payload)
        print(mechanic.__dict__)
        # print(dir(mechanic))
        mechanic_dict = model_to_dict(mechanic)

        return jsonify(data = mechanic_dict, status = {"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error creating the resources"})

# Show route
@mechanic.route('/<id>', methods=["GET"])
def get_one_mechanic(id):
    try:
        mechanic = models.Mechanic.get_by_id(id)
        print(mechanic)
        mechanic_dict = model_to_dict(mechanic)
        return jsonify(data = mechanic_dict, status={"code": 200, "message": f"Found mechanic with id {mechanic.id}"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting one resource"})

# Update route
@mechanic.route('/<id>', methods=["PUT"])
def update_mechanic(id):
    try:
        payload = request.get_json()
        # type subtitution property 'owner' of mechanic from dict to int
        # payload['owner'] = current_user.id

        query = models.Mechanic.update(**payload).where(models.Mechanic.id == id)
        query.execute()
        updated_mechanic = model_to_dict(models.Mechanic.get_by_id(id))
        return jsonify(data=updated_mechanic, status={"code": 200, "message": f"Resourced updated successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error updating one resource"})

# Delete route
@mechanic.route('/<id>', methods=["DELETE"])
def delete_mechanic(id):
    try:
        query = models.Mechanic.delete().where(models.Mechanic.id == id)
        query.execute()
        return jsonify(data='Resource successfully deleted', status={"code": 200, "message": "Resource successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error deleting resource"})        