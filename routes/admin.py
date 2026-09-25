from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

from models.user import User
from models.order import Order, OrderItem
from models.product import Product

from extensions import db

import os
import uuid


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


ALLOWED_IMAGE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def allowed_image(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_IMAGE_EXTENSIONS
    )


def save_product_image(image_file):

    if not image_file:

        return None


    if image_file.filename == "":

        return None


    if not allowed_image(image_file.filename):

        return None


    original_filename = secure_filename(
        image_file.filename
    )


    extension = original_filename.rsplit(
        ".",
        1
    )[1].lower()


    unique_filename = (
        f"{uuid.uuid4().hex}.{extension}"
    )


    upload_folder = os.path.join(
        "static",
        "images"
    )


    os.makedirs(
        upload_folder,
        exist_ok=True
    )


    image_path = os.path.join(
        upload_folder,
        unique_filename
    )


    image_file.save(
        image_path
    )


    return unique_filename


@admin_bp.before_request
@login_required
def admin_required():

    if current_user.role != "admin":

        flash(
            "You do not have permission to access the admin area."
        )

        return redirect(
            url_for("dashboard.dashboard")
        )


@admin_bp.route("/")
def dashboard():

    orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()
    recent_orders = Order.query.order_by(
    Order.created_at.desc()
    ).limit(5).all()

    total_sales = db.session.query(
        db.func.sum(Order.total_amount)
    ).scalar() or 0

    total_orders = Order.query.count()

    total_customers = User.query.filter_by(
        role="customer"
    ).count()

    total_products = Product.query.count()

    pending_orders = Order.query.filter_by(
        order_status="Pending"
    ).count()

    processing_orders = Order.query.filter_by(
        order_status="Processing"
    ).count()

    out_for_delivery_orders = Order.query.filter_by(
        order_status="Out for Delivery"
    ).count()

    delivered_orders = Order.query.filter_by(
        order_status="Delivered"
    ).count()

    return render_template(
    "admin/dashboard.html",
    orders=orders,
    recent_orders=recent_orders,
    total_sales=total_sales,
    total_orders=total_orders,
    total_customers=total_customers,
    total_products=total_products,
    pending_orders=pending_orders,
    processing_orders=processing_orders,
    out_for_delivery_orders=out_for_delivery_orders,
    delivered_orders=delivered_orders
)

@admin_bp.route("/products")
def products():

    products = Product.query.order_by(
        Product.id.desc()
    ).all()

    return render_template(
        "admin/products.html",
        products=products
    )


@admin_bp.route(
    "/products/add",
    methods=["GET", "POST"]
)
def add_product():

    if request.method == "POST":

        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")

        price_300ml = request.form.get(
            "price_300ml"
        )

        price_500ml = request.form.get(
            "price_500ml"
        )

        price_1liter = request.form.get(
            "price_1liter"
        )

        stock = request.form.get("stock")


        if (
            not name
            or not description
            or not category
            or not price_300ml
            or not price_500ml
            or not price_1liter
            or not stock
        ):

            flash(
                "Please fill in all required fields."
            )

            return redirect(
                url_for("admin.add_product")
            )


        try:

            price_300ml = float(price_300ml)
            price_500ml = float(price_500ml)
            price_1liter = float(price_1liter)

            stock = int(stock)

        except ValueError:

            flash(
                "Please enter valid prices and stock quantity."
            )

            return redirect(
                url_for("admin.add_product")
            )


        if (
            price_300ml < 0
            or price_500ml < 0
            or price_1liter < 0
            or stock < 0
        ):

            flash(
                "Prices and stock cannot be negative."
            )

            return redirect(
                url_for("admin.add_product")
            )


        image_file = request.files.get(
            "image"
        )


        image_filename = None


        if image_file and image_file.filename:

            if not allowed_image(
                image_file.filename
            ):

                flash(
                    "Invalid image format. Use JPG, JPEG, PNG or WEBP."
                )

                return redirect(
                    url_for("admin.add_product")
                )


            image_filename = save_product_image(
                image_file
            )


        product = Product(

            name=name,

            description=description,

            category=category,

            price_300ml=price_300ml,

            price_500ml=price_500ml,

            price_1liter=price_1liter,

            stock=stock,

            image=image_filename

        )


        db.session.add(product)

        db.session.commit()


        flash(
            f"{product.name} was added successfully."
        )


        return redirect(
            url_for("admin.products")
        )


    categories = [
        "Mango Juice",
        "Passion Juice",
        "Orange Juice",
        "Pineapple Juice",
        "Watermelon Juice",
        "Mixed Fruit",
        "Detox",
        "Smoothies"
    ]


    return render_template(
        "admin/add_product.html",
        categories=categories
    )


@admin_bp.route(
    "/products/<int:product_id>/edit",
    methods=["GET", "POST"]
)
def edit_product(product_id):

    product = Product.query.get_or_404(
        product_id
    )


    categories = [
        "Mango Juice",
        "Passion Juice",
        "Orange Juice",
        "Pineapple Juice",
        "Watermelon Juice",
        "Mixed Fruit",
        "Detox",
        "Smoothies"
    ]


    if request.method == "POST":

        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")

        price_300ml = request.form.get(
            "price_300ml"
        )

        price_500ml = request.form.get(
            "price_500ml"
        )

        price_1liter = request.form.get(
            "price_1liter"
        )

        stock = request.form.get("stock")


        if (
            not name
            or not description
            or not category
            or not price_300ml
            or not price_500ml
            or not price_1liter
            or not stock
        ):

            flash(
                "Please fill in all required fields."
            )

            return redirect(
                url_for(
                    "admin.edit_product",
                    product_id=product.id
                )
            )


        try:

            price_300ml = float(price_300ml)
            price_500ml = float(price_500ml)
            price_1liter = float(price_1liter)

            stock = int(stock)

        except ValueError:

            flash(
                "Please enter valid prices and stock quantity."
            )

            return redirect(
                url_for(
                    "admin.edit_product",
                    product_id=product.id
                )
            )


        if (
            price_300ml < 0
            or price_500ml < 0
            or price_1liter < 0
            or stock < 0
        ):

            flash(
                "Prices and stock cannot be negative."
            )

            return redirect(
                url_for(
                    "admin.edit_product",
                    product_id=product.id
                )
            )


        image_file = request.files.get(
            "image"
        )


        if image_file and image_file.filename:

            if not allowed_image(
                image_file.filename
            ):

                flash(
                    "Invalid image format. Use JPG, JPEG, PNG or WEBP."
                )

                return redirect(
                    url_for(
                        "admin.edit_product",
                        product_id=product.id
                    )
                )


            new_image = save_product_image(
                image_file
            )


            if new_image:

                product.image = new_image


        product.name = name

        product.description = description

        product.category = category

        product.price_300ml = price_300ml

        product.price_500ml = price_500ml

        product.price_1liter = price_1liter

        product.stock = stock


        db.session.commit()


        flash(
            f"{product.name} was updated successfully."
        )


        return redirect(
            url_for("admin.products")
        )


    return render_template(
        "admin/edit_product.html",
        product=product,
        categories=categories
    )


@admin_bp.route(
    "/products/<int:product_id>/delete",
    methods=["POST"]
)
def delete_product(product_id):

    product = Product.query.get_or_404(
        product_id
    )


    existing_order_item = OrderItem.query.filter_by(
        product_id=product.id
    ).first()


    if existing_order_item:

        flash(
            f"{product.name} cannot be deleted because it has already been included in an order."
        )

        return redirect(
            url_for("admin.products")
        )


    product_name = product.name


    db.session.delete(product)

    db.session.commit()


    flash(
        f"{product_name} was deleted successfully."
    )


    return redirect(
        url_for("admin.products")
    )


@admin_bp.route(
    "/orders/<int:order_id>/status",
    methods=["POST"]
)
def update_order_status(order_id):

    order = Order.query.get_or_404(
        order_id
    )


    new_status = request.form.get(
        "order_status"
    )


    allowed_statuses = [
        "Pending",
        "Processing",
        "Out for Delivery",
        "Delivered"
    ]


    if new_status not in allowed_statuses:

        flash(
            "Invalid order status."
        )

        return redirect(
            url_for("admin.dashboard")
        )


    order.order_status = new_status

    db.session.commit()


    flash(
        f"Order #{order.id} status updated to {new_status}."
    )


    return redirect(
        url_for("admin.dashboard")
    )


@admin_bp.route("/customers")
def customers():

    search = request.args.get("search", "").strip()


    query = User.query


    if search:

        query = query.filter(
            db.or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.phone.ilike(f"%{search}%")
            )
        )


    customers = query.order_by(
        User.id.desc()
    ).all()


    return render_template(
        "admin/customers.html",
        customers=customers,
        search=search
    )
@admin_bp.route(
    "/customers/<int:user_id>/toggle-status",
    methods=["POST"]
)
def toggle_customer_status(user_id):

    customer = User.query.get_or_404(user_id)

    if customer.role == "admin":
        flash(
            "Admin accounts cannot be disabled from this page."
        )

        return redirect(
            url_for("admin.customers")
        )

    customer.is_active = not customer.is_active

    db.session.commit()

    if customer.is_active:
        flash(
            f"{customer.name}'s account has been activated."
        )
    else:
        flash(
            f"{customer.name}'s account has been disabled."
        )

    return redirect(
        url_for("admin.customers")
    )

@admin_bp.route(
    "/customers/<int:user_id>/edit",
    methods=["GET", "POST"]
)
def edit_customer(user_id):

    customer = User.query.get_or_404(user_id)

    if customer.role == "admin":
        flash(
            "Admin accounts cannot be edited from this page."
        )

        return redirect(
            url_for("admin.customers")
        )

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        if not name or not email or not phone:

            flash(
                "Please fill in all customer information."
            )

            return redirect(
                url_for(
                    "admin.edit_customer",
                    user_id=customer.id
                )
            )

        existing_email = User.query.filter(
            User.email == email,
            User.id != customer.id
        ).first()

        if existing_email:

            flash(
                "Another customer is already using that email."
            )

            return redirect(
                url_for(
                    "admin.edit_customer",
                    user_id=customer.id
                )
            )

        existing_phone = User.query.filter(
            User.phone == phone,
            User.id != customer.id
        ).first()

        if existing_phone:

            flash(
                "Another customer is already using that phone number."
            )

            return redirect(
                url_for(
                    "admin.edit_customer",
                    user_id=customer.id
                )
            )

        customer.name = name
        customer.email = email
        customer.phone = phone

        db.session.commit()

        flash(
            f"{customer.name}'s information was updated successfully."
        )

        return redirect(
            url_for("admin.customers")
        )

    return render_template(
        "admin/edit_customer.html",
        customer=customer
    )