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
        return jsonify(data = updated_user, status = {"code": 200, "message": "Succesfully updated user"})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {"code": 400, "message": "User update failed"})
        
# delete route
@user.route('/<id>', methods=["DELETE"])
def user_delete(id):
    try:
        user = models.User.get_by_id(id)
        user_dict = model_to_dict(user)
        print(user_dict)
        query = models.User.delete().where(models.User.id == id)
        print(query)
        query.execute()
        delete_prob = models.Problem.delete().where(models.Problem.owner_username == user_dict["username"])
        delete_prob.execute()
        print(delete_prob)
        return jsonify(data = "User and Problems successfully deleted", status = {"code": 200, "message": "Group successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data = {}, status = {"code": 400, "message": "Failed to delete the group from the database"})







