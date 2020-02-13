from flask import Flask, jsonify, g
from flask_login import LoginManager
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = 'mysecretkey'
login_manager = LoginManager()
login_manager.init_app(app)

import models

from resources.patients import patients
from resources.providers import providers

@login_manager.user_loader
def load_user(userid):
    try:
        return models.Patient.get(models.Patient.id == userid)
    except models.DoesNotExist:
        return none


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(
        data = {
            'error': 'User not logged in'
        },
        status = {
            'code': 401,
            'message': 'You must be logged in to access your site'
        }
    )

CORS(patients, origin=['http://localhost:3000'], supports_credentials = True)
CORS(providers, origin=['http://localhost:3000'], supports_credentials = True)


app.register_blueprint(patients, url_prefix='/api/v1/patients')
app.register_blueprint(providers, url_prefix='/api/v1/providers')


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
    return 'welcome'




DEBUG = True
PORT = 8000
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)