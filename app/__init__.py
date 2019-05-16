from datetime import timedelta

from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.secret_key = 'secret key'
from app.config import Config
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#from app import routes, models, errors, logs
from app import routes, errors, models
#app.config.from_object(Config)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)