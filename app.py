from flask import Flask, jsonify, g
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

CORS(mechanic, origin=['http://localhost:3000'], supports_credentials=True)
CORS(user, origin=['http://localhost:3000'], supports_credentials=True)
CORS(problem, origin=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(mechanic, url_prefix='/api/v1/mechanic')
app.register_blueprint(user, url_prefix='/api/v1/user')
app.register_blueprint(mechanic, url_prefix='/api/v1/problem')


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


