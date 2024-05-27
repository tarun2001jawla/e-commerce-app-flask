from website import create_app
from website.routes import home_bp, product_bp, basket_bp, checkout_bp,auth_bp

app = create_app()

app.config['SECRET_KEY'] = '123'

# Register Blueprints with the Flask app
app.register_blueprint(home_bp)
app.register_blueprint(product_bp)
app.register_blueprint(basket_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)