from flask import Flask, jsonify, g
from flask_login import LoginManager
from flask_cors import CORS
app = Flask(__name__)
app.secret_key = 'mysecretkey'
login_manager = LoginManager()
login_manager.init_app(app)

import models
