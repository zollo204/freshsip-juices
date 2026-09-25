from flask import Blueprint, render_template, session, redirect, url_for, request
from models.product import Product


cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart")
def cart():

    cart_items = session.get("cart", [])

    items = []
    total = 0

    for item in cart_items:

        product = Product.query.get(item["product_id"])

        if product:

            if item["size"] == "300ml":
                price = product.price_300ml

            elif item["size"] == "500ml":
                price = product.price_500ml

            else:
                price = product.price_1liter

            quantity = item["quantity"]

            subtotal = price * quantity

            items.append({
                "product": product,
                "size": item["size"],
                "price": price,
                "quantity": quantity,
                "subtotal": subtotal
            })

            total += subtotal

    return render_template(
        "cart.html",
        items=items,
        total=total
    )


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    size = request.form.get("size")
    quantity = int(request.form.get("quantity", 1))

    product = Product.query.get_or_404(product_id)

    if size not in ["300ml", "500ml", "1 Liter"]:
        return redirect(url_for("shop.shop"))

    if quantity < 1:
        quantity = 1

    cart = session.get("cart", [])

    found = False

    for item in cart:

        if (
            item["product_id"] == product_id
            and item["size"] == size
        ):
            item["quantity"] += quantity
            found = True
            break

    if not found:

        cart.append({
            "product_id": product_id,
            "size": size,
            "quantity": quantity
        })

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart.cart"))


@cart_bp.route(
    "/cart/update/<int:product_id>/<size>",
    methods=["POST"]
)
def update_cart(product_id, size):

    quantity = int(request.form.get("quantity", 1))

    if quantity < 1:
        return redirect(
            url_for(
                "cart.remove_from_cart",
                product_id=product_id,
                size=size
            )
        )

    cart = session.get("cart", [])

    for item in cart:

        if (
            item["product_id"] == product_id
            and item["size"] == size
        ):
            item["quantity"] = quantity
            break

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart.cart"))


@cart_bp.route("/cart/remove/<int:product_id>/<size>")
def remove_from_cart(product_id, size):

    cart = session.get("cart", [])

    cart = [
        item for item in cart
        if not (
            item["product_id"] == product_id
            and item["size"] == size
        )
    ]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart.cart"))


@cart_bp.route("/cart/clear")
def clear_cart():

    session["cart"] = []

    return redirect(url_for("cart.cart"))
