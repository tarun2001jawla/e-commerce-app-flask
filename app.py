from flask import Flask
from flask_bootstrap import Bootstrap
from website.routes import home_bp, product_bp, basket_bp, checkout_bp
from website import db

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'

bootstrap = Bootstrap(app)
db.init_app(app)

# Register the Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(product_bp)
app.register_blueprint(basket_bp)
app.register_blueprint(checkout_bp)

if __name__ == '__main__':
    app.run()