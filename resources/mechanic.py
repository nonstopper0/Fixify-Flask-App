from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

mechanic = Blueprint('mechanic', 'mechanic')

@mechanic.route('/<id>', methods=["GET"])
def get_one_mechanic(id):
    try:
        mechanic = models.Mechanic.get_by_id(id)
        mechanic_dict = model_to_dict(mechanic)
        return jsonify(data = mechanic_dict , status={"code": 200, "message": "User found"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error, User not found"})
    except: 
        print('big exception')

# update route

# Index route
# @mechanic.route('/', methods=["GET"])
# def get_all_mechanic():
#     try:
#         mechanic = [model_to_dict(mechanic) for mechanic in models.Mechanic.select()]
#         print(mechanic)
#         for mechanic in mechanic:
#             mechanic.pop('password')
#         return jsonify(data = mechanic, status={"code": 200, "message": "Success"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 400, "message": "Error getting the index"})

# Update route
@mechanic.route('/<id>', methods=["PUT"])
def update_mechanic(id):
    try:
        payload = request.get_json()
        print(payload)
        query = models.Mechanic.update(**payload).where(models.Mechanic.id == id)
        query.execute()
        updated_mechanic = model_to_dict(models.Mechanic.get_by_id(id))
        return jsonify(data = updated_mechanic, status = {"code": 200, "message": "Mechanic profile updated successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error updating the mechanic"})

# Delete route
@mechanic.route('/<id>', methods=["DELETE"])
def delete_mechanic(id):
    try:
        query = models.Mechanic.delete().where(models.Mechanic.id == id)
        mechanic_delete = models.Problem.mechanic_username
        del mechanic_delete
        query.execute()
        return jsonify(data='Resource successfully deleted', status={"code": 200, "message": "Mechanic successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error deleting the mechanic from the database"})