from flask import Flask, jsonify, g, request
from flask_login import LoginManager
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = 'thisisasecretkey'
login_manager = LoginManager()
login_manager.init_app(app)

import models
from resources.mechanic import mechanic
from resources.user import user
from resources.problem import problem

# @login_manager.user_loader
# def load_user(userid):
#     try:
#         return models.User.get(models.User.id == userid)
#     except models.DoesNotExist:
#         return None

# @login_manager.unauthorized_handler
# def unauthorized():
#     return jsonify(
#         data = {
#             'error': 'User not logged in.'
#         },
#         status = {
#             'code': 401,
#             'message': 'You must be logged in to access that resource.'
#         }
#     )

CORS(mechanic, origin=['http://localhost:3000'], supports_credentials=True)
CORS(user, origin=['http://localhost:3000'], supports_credentials=True)
CORS(problem, origin=['http://localhost:3000'], supports_credentials=True)
CORS(app, supports_credentials=True)

app.register_blueprint(mechanic, url_prefix='/mechanic')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(mechanic, url_prefix='/problem')


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

@app.route('/login', methods=['POST']) 
def login():
    return "hi"

@app.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    payload['email'].lower()
    payload['username'].lower()
    payload['type'].lower()
    try:
        if payload['type'] == 'user':
            print('user')
        elif payload['type'] == 'mechanic':
            print('mechanic')
        return jsonify(data ={}, status = {"code": 200, "message": "Success"})
    except:
        return jsonify(data={}, status={"code": 400, "message": "Error creating the resources"})



DEBUG = True
PORT = 8000
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)


