from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.order import Order


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    latest_order = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Order.created_at.desc()
    ).first()


    return render_template(
        "dashboard.html",
        user=current_user,
        latest_order=latest_order
    )