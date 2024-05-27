from website import create_app, db
from website.models import Product

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()

    # Insert initial product data
    products = [
        Product(name='Apple iPhone 14', price=999.99, description='The latest iPhone with A15 Bionic chip and advanced dual-camera system.'),
        Product(name='Samsung Galaxy S22', price=799.99, description='Samsung\'s flagship smartphone with a dynamic AMOLED display and powerful Exynos processor.'),
        Product(name='Sony WH-1000XM4', price=349.99, description='Industry-leading noise canceling headphones with exceptional sound quality and comfort.'),
        Product(name='Apple MacBook Pro', price=1299.99, description='High-performance MacBook Pro with M1 chip, Retina display, and all-day battery life.'),
        Product(name='Dell XPS 13', price=1099.99, description='Ultra-thin and light laptop with InfinityEdge display, Intel i7 processor, and long battery life.')
    ]

    # Add the products to the session and commit them to the database
    db.session.bulk_save_objects(products)
    db.session.commit()

    print("Database and tables created with initial product data!")
