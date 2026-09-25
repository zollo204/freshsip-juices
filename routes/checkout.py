from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    current_app,
    flash
)

from flask_login import login_required, current_user

from models.product import Product
from models.order import Order, OrderItem

from extensions import db


checkout_bp = Blueprint(
    "checkout",
    __name__
)


@checkout_bp.route(
    "/checkout",
    methods=["GET", "POST"]
)
@login_required
def checkout():

    cart_items = session.get(
        "cart",
        []
    )

    if not cart_items:

        flash(
            "Your cart is empty."
        )

        return redirect(
            url_for("cart.cart")
        )


    items = []

    total = 0


    # =============================
    # BUILD CART ITEMS
    # =============================

    for item in cart_items:

        product = Product.query.get(
            item["product_id"]
        )

        if not product:
            continue


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


    if not items:

        flash(
            "Your cart contains unavailable products."
        )

        return redirect(
            url_for("cart.cart")
        )


    # =============================
    # PLACE ORDER
    # =============================

    if request.method == "POST":

        delivery_method = request.form.get(
            "delivery_method"
        )

        delivery_address = request.form.get(
            "delivery_address"
        )

        payment_method = request.form.get(
            "payment_method"
        )


        # =============================
        # CHECK CHECKOUT FIELDS
        # =============================

        if (
            not delivery_method
            or not delivery_address
            or not payment_method
        ):

            flash(
                "Please complete all checkout fields."
            )

            return redirect(
                url_for("checkout.checkout")
            )


        # =============================
        # CHECK AVAILABLE STOCK
        # =============================

        requested_stock = {}


        for item in items:

            product_id = item["product"].id

            requested_stock[product_id] = (
                requested_stock.get(
                    product_id,
                    0
                )
                + item["quantity"]
            )


        for product_id, quantity in requested_stock.items():

            product = Product.query.get(
                product_id
            )

            if not product:
                continue


            if quantity > product.stock:

                flash(
                    f"Only {product.stock} units of "
                    f"{product.name} are currently available. "
                    f"Please adjust your cart."
                )

                return redirect(
                    url_for("cart.cart")
                )


        # =============================
        # CREATE ORDER
        # =============================

        order = Order(

            user_id=current_user.id,

            total_amount=total,

            delivery_method=delivery_method,

            delivery_address=delivery_address,

            payment_method=payment_method,

            payment_status="Pending",

            order_status="Pending"

        )


        db.session.add(
            order
        )


        db.session.flush()


        # =============================
        # CREATE ORDER ITEMS
        # =============================

        for item in items:

            order_item = OrderItem(

                order_id=order.id,

                product_id=item["product"].id,

                product_name=item["product"].name,

                size=item["size"],

                quantity=item["quantity"],

                price=item["price"],

                subtotal=item["subtotal"]

            )


            db.session.add(
                order_item
            )


        # =============================
        # REDUCE PRODUCT STOCK
        # =============================

        for product_id, quantity in requested_stock.items():

            product = Product.query.get(
                product_id
            )

            if product:

                product.stock -= quantity


        # =============================
        # SAVE EVERYTHING
        # =============================

        try:

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            print(
                "CHECKOUT ERROR:",
                error
            )

            flash(
                "There was a problem placing your order. "
                "Please try again."
            )

            return redirect(
                url_for("checkout.checkout")
            )


        # =============================
        # CLEAR CART
        # =============================

        session["cart"] = []

        session.modified = True


        flash(
            f"Order #{order.id} placed successfully!"
        )


        return redirect(
            url_for(
                "checkout.order_confirmation",
                order_id=order.id
            )
        )


    # =============================
    # DISPLAY CHECKOUT PAGE
    # =============================

    return render_template(

        "checkout.html",

        items=items,

        total=total,

        paybill=current_app.config[
            "MPESA_PAYBILL"
        ],

        account=current_app.config[
            "MPESA_ACCOUNT"
        ]

    )


@checkout_bp.route(
    "/order-confirmation/<int:order_id>"
)
@login_required
def order_confirmation(order_id):

    order = Order.query.get_or_404(
        order_id
    )


    if order.user_id != current_user.id:

        flash(
            "You are not allowed to view this order."
        )

        return redirect(
            url_for("dashboard.dashboard")
        )


    return render_template(

        "order_confirmation.html",

        order=order

    )