from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

problem = Blueprint('problem', 'problem')



# Index route
@problem.route('/', methods=["GET"])
def all_problems():
    try:
        problem = [model_to_dict(problem) for problem in models.Problem.select()]
        return jsonify(data = problem, status={"code": 200, "message": "Got the problems"})
    except models.DoesNotExist:
        return jsonify(data = {}, status={"code": 400, "message": "Error getting the problems"})

# Create route
@problem.route('/', methods=["POST"])
def create_problem():
    try:
        payload = request.get_json()
        problem = models.Problem.create(**payload)
        problem_dict = model_to_dict(problem)

        return jsonify(data = {}, status = {"code": 200, "message": "Problem added"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error creating the problem"})

# show route
@problem.route('/<id>', methods=["GET"])
def get_one_problem(id):
    try:
        problem = models.Problem.get_by_id(id)
        problem_dict = model_to_dict(problem)
        return jsonify(data = problem_dict, status={"code": 200, "message": f"Found the problem {problem.id}"})
    except models.DoesNotExist:
        return jsonify(data = {}, status={"code": 400, "message": "Error finding the problem"})

# update route
@problem.route('/<id>', methods=["PUT"])
def update_problem(id):
    try:
        payload = request.get_json()
        query = models.Problem.update(**payload).where(models.Problem.id == id)
        query.execute()
        updated_problem = model_to_dict(models.Problem.get_by_id(id))
        return jsonify(data = updated_problem, status = {"code": 200, "message": "Information updated successfully"})
    except models.DoesNotExist:
        return jsonify(data = {}, status={"code": 400, "messsage": "Error in update"})

# delete route
@problem.route('/<id>', methods=["DELETE"])
def delete_problem(id):
    try:
        query = models.Problem.delete().where(models.Problem.id == id)
        query.execute()
        return jsonify(data = "Problem succesfully deleted", status={"code": 200, "message": "Problem successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data = {}, status={"code": 400, "message": "Failed to delete"})
        
