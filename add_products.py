from app import app, db
from models.product import Product


with app.app_context():

    products = [
        Product(
            name="Mango Juice",
            description="Sweet and refreshing natural mango juice.",
            category="Mango Juice",
            price_300ml=120,
            price_500ml=180,
            price_1liter=300,
            stock=50,
            image="mango.jpg"
        ),

        Product(
            name="Passion Juice",
            description="Refreshing passion fruit juice packed with flavor.",
            category="Passion Juice",
            price_300ml=120,
            price_500ml=180,
            price_1liter=300,
            stock=50,
            image="passion.jpg"
        ),

        Product(
            name="Orange Juice",
            description="Freshly squeezed orange juice full of goodness.",
            category="Orange Juice",
            price_300ml=130,
            price_500ml=190,
            price_1liter=320,
            stock=50,
            image="orange.jpg"
        ),

        Product(
            name="Pineapple Juice",
            description="Fresh tropical pineapple juice.",
            category="Pineapple Juice",
            price_300ml=130,
            price_500ml=190,
            price_1liter=320,
            stock=40,
            image="pineapple.jpg"
        ),

        Product(
            name="Watermelon Juice",
            description="Cool and refreshing watermelon juice.",
            category="Watermelon Juice",
            price_300ml=120,
            price_500ml=180,
            price_1liter=300,
            stock=40,
            image="watermelon.jpg"
        )
    ]

    db.session.add_all(products)
    db.session.commit()

    print("Products added successfully!")