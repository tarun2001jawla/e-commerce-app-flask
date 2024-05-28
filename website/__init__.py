from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='C:/Users/Tarun/Desktop/Office Work/e-commerce_using_python_flask/static')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'
    app.config['SECRET_KEY'] = '123'

    bootstrap.init_app(app)
    db.init_app(app)

    from website import models, routes

    with app.app_context():
        db.create_all()  # Create the database tables

    return app


