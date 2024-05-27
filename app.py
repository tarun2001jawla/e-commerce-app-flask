from flask import Flask
from website.routes import home_bp, product_bp, basket_bp, checkout_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'

# Register Blueprints with the Flask app
app.register_blueprint(home_bp)
app.register_blueprint(product_bp)
app.register_blueprint(basket_bp)
app.register_blueprint(checkout_bp)

# Other configurations and imports...

if __name__ == '__main__':
    app.run(debug=True ,port=8080,use_reloader=False)
    
