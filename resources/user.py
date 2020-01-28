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
