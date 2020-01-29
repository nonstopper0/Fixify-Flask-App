from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

user = Blueprint('user', 'user')


@user.route('/<id>', methods=["GET"])
def get_one_user(id):
    try:
        user = models.User.get_by_id(id)
        user_dict = model_to_dict(user)
        return jsonify(data = user_dict , status={"code": 200, "message": "User found"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error, User not found"})

# update route
@user.route('/<id>', methods=["PUT"])
def update_user(id):
    try:
        payload = request.get_json()
        print(payload)
        query = models.User.update(**payload).where(models.User.id == id)
        query.execute()
        updated_user = model_to_dict(models.User.get_by_id(id))
        del updated_user['password']
        return jsonify(data = updated_user, status = {"code": 200, "message": "Succesfully updated user"})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {"code": 400, "message": "User update failed"})


# delete route
@user.route('/<id>', methods=["DELETE"])
def user_delete(id):
    try:
        query = models.User.delete().where(models.User.id == id)
        query.execute()
        return jsonify(data = "User successfully deleted", status = {"code": 200, "message": "User successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {"code": 400, "message": "Failed to delete the user from the database"})



