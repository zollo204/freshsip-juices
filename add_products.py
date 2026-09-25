from app import app, db
from models.product import Product


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
        price_300ml=120,
        price_500ml=180,
        price_1liter=300,
        stock=50,
        image="orange.jpg"
    ),

    Product(
        name="Pineapple Juice",
        description="Fresh tropical pineapple juice.",
        category="Pineapple Juice",
        price_300ml=120,
        price_500ml=180,
        price_1liter=300,
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
    ),

    Product(
        name="Sugarcane Ginger Lemon",
        description="Naturally sweet sugarcane blended with zesty lemon and fresh ginger for a balanced sweet and tangy refreshment.",
        category="Detox Juices",
        price_300ml=120,
        price_500ml=180,
        price_1liter=300,
        stock=50,
        image="sugarcane.jpg"
    ),

    Product(
        name="Tamarind Ginger",
        description="Tangy tamarind blended with warming ginger for a bold and refreshing natural juice.",
        category="Detox Juices",
        price_300ml=120,
        price_500ml=180,
        price_1liter=300,
        stock=50,
        image="tamarind.jpg"
    ),

    Product(
        name="Beetroot Carrot Apple",
        description="Earthy beetroot combined with sweet carrot and fruity apple for a smooth and refreshing natural blend.",
        category="Detox Juices",
        price_300ml=120,
        price_500ml=180,
        price_1liter=300,
        stock=50,
        image="beetroot.jpg"
    ),

    Product(
        name="Carrot Ginger Lemon",
        description="Sweet carrot blended with warm ginger and bright lemon for a balanced sweet, warm and citrusy juice.",
        category="Detox Juices",
        price_300ml=120,
        price_500ml=180,
        price_1liter=300,
        stock=50,
        image="carrot.jpg"
    )
]


with app.app_context():

    for product in products:

        existing_product = Product.query.filter_by(
            name=product.name
        ).first()

        if existing_product:
            existing_product.description = product.description
            existing_product.category = product.category
            existing_product.price_300ml = product.price_300ml
            existing_product.price_500ml = product.price_500ml
            existing_product.price_1liter = product.price_1liter
            existing_product.stock = product.stock
            existing_product.image = product.image

        else:
            db.session.add(product)

    db.session.commit()

    print("Products added/updated successfully!")