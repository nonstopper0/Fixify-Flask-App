# from flask import Flask, jsonify, g
# from flask_login import LoginManager
# from flask_cors import CORS
# app = Flask(__name__)
# app.secret_key = 'thisisasecretkey'
# login_manager = LoginManager()
# login_manager.init_app(app)

import models
from resources.dogs import dogs
from resources.users import users

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(
        data = {
            'error': 'User not logged in.'
        },
        status = {
            'code': 401,
            'message': 'You must be logged in to access that resource.'
        }
    )

CORS(dogs, origin=['http://localhost:3000'], supports_credentials=True)
CORS(users, origin=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(dogs, url_prefix='/api/v1/dogs')
app.register_blueprint(users, url_prefix='/api/v1/users')



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


DEBUG = True
PORT = 8000
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)