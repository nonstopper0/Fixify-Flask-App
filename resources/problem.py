from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

problem = Blueprint('problem', 'problem')

# Index route
@problem.route('/', methods=["GET"])
def all_problems():
    try:
        problem = [model_to_dict(problem) for problem in models.Problem.select().where(models.Problem.owner_id == current_user.id)]
        print(problem)
        for problem in problem:
            problem['owner'].pop('password')
        return jsonify(data = problem, status={"code": 200, "message": "Got the problems"})
    except models.DoesNotExist:
        return jsonify(data = {}, status={"code": 400, "message": "Error getting the problems"})

# Create route
@problem.route('/', methods=["POST"])
def create_problem():
    try:
        payload = request.get_json()
        payload['owner'] = current_user.id
        problem = models.Problem.create(**payload)
        problem_dict = model_to_dict(problem)

        return jsonify(data = problem_dict, status = {"code": 200, "message": "Problem added"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error creating the problem"})

