from . import db

from website import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=True)  # Add author column
    price = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'price': self.price,
            'isbn': self.isbn,
            'description': self.description
        }





from website import db

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Text, unique=True, nullable=False)
    customer_name = db.Column(db.Text, nullable=False)
    customer_email = db.Column(db.Text, nullable=False)
    customer_phone = db.Column(db.Text)
    customer_state = db.Column(db.Text)
    customer_city = db.Column(db.Text)
    customer_zip = db.Column(db.Text)
    order_date = db.Column(db.DateTime, nullable=False)
    expected_delivery_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Order(order_id={self.order_id}, customer_name={self.customer_name})'

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

