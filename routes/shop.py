from flask import Blueprint, render_template, request
from models.product import Product


shop_bp = Blueprint("shop", __name__)


@shop_bp.route("/shop")
def shop():

    category = request.args.get("category")
    search = request.args.get("search")

    query = Product.query

    if category:
        query = query.filter_by(category=category)

    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    products = query.all()

    categories = [
        "Mango Juice",
        "Passion Juice",
        "Orange Juice",
        "Pineapple Juice",
        "Watermelon Juice"
    ]

    return render_template(
        "shop.html",
        products=products,
        categories=categories,
        selected_category=category,
        search=search
    )
@shop_bp.route("/product/<int:product_id>")
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template(
        "product.html",
        product=product
    )  