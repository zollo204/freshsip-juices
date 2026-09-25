from extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(50), nullable=False)

    price_300ml = db.Column(db.Float, nullable=False)
    price_500ml = db.Column(db.Float, nullable=False)
    price_1liter = db.Column(db.Float, nullable=False)

    stock = db.Column(db.Integer, default=0, nullable=False)

    image = db.Column(db.String(255))

    def __repr__(self):
        return f"<Product {self.name}>"