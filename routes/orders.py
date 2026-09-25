from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.order import Order


orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders")
@login_required
def orders():

    customer_orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=customer_orders
    )


@orders_bp.route("/orders/<int:order_id>/tracking")
@login_required
def track_order(order_id):

    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:

        return "Unauthorized", 403

    return render_template(
        "tracking.html",
        order=order
    )