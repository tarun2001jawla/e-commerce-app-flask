from flask import Blueprint, render_template, redirect, url_for, flash, request
from website.forms import SearchForm, SignupForm, LoginForm
from website import db, bcrypt
from website.models import User, Product
from flask import session
from datetime import datetime, timedelta
import string
import random
from website import db
from website.models import User, Product, Order

def generate_random_order_id():
    # Generate a random string of length 8 with alphanumeric characters
    characters = string.ascii_letters + string.digits
    order_id = ''.join(random.choice(characters) for _ in range(8))
    return order_id

# Define a Blueprint for home routes
home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    products = Product.query.all()
    form = SearchForm()
    login_form = LoginForm()
    signup_form = SignupForm()
    if form.validate_on_submit():
        query = form.query.data
        products = Product.query.filter(...).all()  # Implement actual search/filter logic here
        return render_template('index.html', form=form, products=products)
    return render_template('home.html', form=form, login_form=login_form, signup_form=signup_form, products=products)

# Define a Blueprint for product route
product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)

# Define a Blueprint for basket route
basket_bp = Blueprint('basket', __name__, url_prefix='/basket')

@basket_bp.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', title='Your Cart', cart_items=cart_items)

# add to cart routes
@basket_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if product:
        cart_items = session.get('cart', [])
        cart_items.append(product.to_dict())
        session['cart'] = cart_items
    return redirect(url_for('basket.cart'))

# Define a Blueprint for checkout route
checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@checkout_bp.route('/', methods=['GET', 'POST'])
def checkout():
    return render_template('checkout.html')

@checkout_bp.route('/complete_order', methods=['POST'])
def complete_order():
    # Retrieve form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    state = request.form.get('state')
    city = request.form.get('city')
    zip_code = request.form.get('zip')

    # Debugging: print form data to console
    print("Form data:", name, email, phone, state, city, zip_code)

    if not all([name, email, phone, state, city, zip_code]):
        # Handle missing form data
        flash('Please fill out all fields.')
        return redirect(url_for('cart'))

    # Generate a random order ID
    order_id = generate_random_order_id()

    # Calculate the expected delivery date (5 days from now)
    expected_delivery_date = datetime.now() + timedelta(days=5)

    # Store order and customer details in the database
    order = Order(
        order_id=order_id,
        customer_name=name,
        customer_email=email,
        customer_phone=phone,
        customer_state=state,
        customer_city=city,
        customer_zip=zip_code,
        order_date=datetime.now(),
        expected_delivery_date=expected_delivery_date
    )
    db.session.add(order)
    db.session.commit()

    # Clear the cart from the session
    session.pop('cart', None)

    # Render the order confirmation page
    return render_template('order_confirmation.html', order_id=order_id, expected_delivery_date=expected_delivery_date)


# Define a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        existing_user = User.query.filter_by(email=signup_form.email.data).first()
        if existing_user is None:
            hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode('utf-8')
            user = User(username=signup_form.username.data, email=signup_form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email address already exists. Please use a different email.', 'danger')
    return render_template('SignupForm.html', title='Signup', signup_form=signup_form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('LoginForm.html', title='Login', login_form=login_form)


