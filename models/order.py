from extensions import db
from datetime import datetime


class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    delivery_method = db.Column(
        db.String(50),
        nullable=False
    )

    delivery_address = db.Column(
        db.Text,
        nullable=False
    )

    payment_method = db.Column(
        db.String(50),
        nullable=False
    )

    payment_status = db.Column(
        db.String(30),
        default="Pending",
        nullable=False
    )

    order_status = db.Column(
        db.String(30),
        default="Pending",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        backref="orders"
    )

    items = db.relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return f"<Order {self.id}>"


class OrderItem(db.Model):

    __tablename__ = "order_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    product_name = db.Column(
        db.String(100),
        nullable=False
    )

    size = db.Column(
        db.String(20),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    subtotal = db.Column(
        db.Float,
        nullable=False
    )

    product = db.relationship(
        "Product"
    )

    def __repr__(self):

        return f"<OrderItem {self.product_name} - {self.size}>"