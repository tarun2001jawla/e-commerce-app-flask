from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from website import models, routes