from flask import Flask, jsonify, g, request
from playhouse.shortcuts import model_to_dict
from flask_login import LoginManager
from flask_cors import CORS
from flask_login import login_user, current_user, logout_user

# At the top
import os

# Just above "if __name__ == '__main__':"
if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

app = Flask(__name__)

app.secret_key = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)

import models

from resources.mechanic import mechanic
from resources.user import user
from resources.problem import problem


CORS(mechanic, origin=['http://localhost:3000/mechanic', 'https://fixify-react-app.herokuapp.com/mechanic'], supports_credentials=True)
CORS(user, origin=['http://localhost:3000/user', 'https://fixify-react-app.herokuapp.com/user'], supports_credentials=True)
CORS(problem, origin=['http://localhost:3000/problem', 'https://fixify-react-app.herokuapp.com//problem'], supports_credentials=True)
CORS(app, supports_credentials=True)

app.register_blueprint(mechanic, url_prefix='/mechanic')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(problem, url_prefix='/problem')


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    return 'hi'

@app.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    if payload['type'] == 'user':
        try:
            models.User.get(models.User.email == payload['email'] or models.User.username == payload['username'])
            return jsonify(data={}, status={"code": 400, "message": "Sorry, you cannot create a user with this email or username"})

        except models.DoesNotExist: 
            print('user register route')
            del payload['type']
            print(payload)
            user = models.User.create(**payload) 
            idOfUser = user.id
            # the status code is what calls the loginfunc on react                
            return jsonify(data = {}, status = {'code': 200, 'message': "Successfully Registered", 'id': idOfUser})
    elif payload['type'] == 'mechanic':
        try:
            models.Mechanic.get(models.Mechanic.email == payload['email'] or models.Mechanic.username == payload['username'])
            return jsonify(data={}, status={"code": 400, "message": "Sorry, you cannot create a user with this email or username"})

        except models.DoesNotExist: 
            print('user register route')
            del payload['type']
            print(payload)
            mechanic = models.Mechanic.create(**payload)  
            idOfMechanic = mechanic.id
            # the status code is what calls the loginfunc on react               
            return jsonify(data = {}, status = {'code': 200, 'message': "Successfully Registered", 'id': idOfMechanic})

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    if payload['type'] == 'user':
        try:
            user = models.User.get(models.User.username == payload['username'])
            userdict = model_to_dict(user)
            if(userdict['password'] == payload['password']):
                del userdict['password']
                idOfUser = userdict['id']
                # the status code is what calls the loginfunc on react 
                return jsonify(data = {}, status = {'code': 200, 'message': "Successfully logged in", 'id': idOfUser})
        
            else:
                return jsonify(data={}, status = {'code': 400, 'message': 'Email or password is incorrect'})
        except models.DoesNotExist:
            return jsonify(data={}, status = {'code': 400, 'message': 'Email or password is incorrect'})
    elif payload['type'] == 'mechanic':
        try:
            mechanic = models.Mechanic.get(models.Mechanic.username == payload['username'])
            mechanicdict = model_to_dict(mechanic)
            if(mechanicdict['password'] == payload['password']):
                del mechanicdict['password']
                idOfMechanic = mechanicdict['id']
                # the status code is what calls the loginfunc on react 
                return jsonify(data = {}, status = {'code': 200, 'message': "Successfully logged in", 'id': idOfMechanic})
            else:
                return jsonify(data={}, status = {'code': 400, 'message': 'Email or password is incorrect'})
        except models.DoesNotExist:
            return jsonify(data={}, status = {'code': 400, 'message': 'Email or password is incorrect'})

@app.route('/logout', methods=['GET'])
def logout():
    logout_user
    return jsonify(data={}, status={'code': 200, 'message': "Succesfully logged out"})

DEBUG = True
PORT = 8000
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)


