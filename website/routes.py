from flask import Blueprint, render_template, redirect, url_for, flash, request
from website.forms import SearchForm, SignupForm, LoginForm
from website import db, bcrypt
from website.models import User, Product
import os

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

@basket_bp.route('/')
def basket():
    return render_template('basket.html')

# Define a Blueprint for checkout route
checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@checkout_bp.route('/', methods=['GET', 'POST'])
def checkout():
    return render_template('checkout.html')

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
