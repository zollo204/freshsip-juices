from flask import Flask, render_template

from config import Config

from extensions import db

from flask_login import LoginManager


login_manager = LoginManager()


def create_app():

    app = Flask(__name__)


    # =============================
    # CONFIGURATION
    # =============================

    app.config.from_object(
        Config
    )


    # =============================
    # DATABASE
    # =============================

    db.init_app(
        app
    )


    # =============================
    # LOGIN
    # =============================

    login_manager.init_app(
        app
    )

    login_manager.login_view = "auth.login"


    # =============================
    # IMPORT MODELS
    # =============================

    from models.user import User

    from models.product import Product

    from models.order import (
        Order,
        OrderItem
    )

    from models.message import Message


    # =============================
    # USER LOADER
    # =============================

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(
            int(user_id)
        )


    # =============================
    # UNREAD MESSAGE COUNT
    # =============================

    @app.context_processor
    def inject_unread_messages():

        unread_messages = 0

        try:

            unread_messages = Message.query.filter_by(
                status="Unread"
            ).count()

        except Exception:

            unread_messages = 0


        return {
            "unread_messages": unread_messages
        }


    # =============================
    # HOME PAGE
    # =============================

    @app.route("/")
    def home():

        featured_products = Product.query.limit(
            10
        ).all()


        return render_template(
            "home.html",
            featured_products=featured_products
        )


    # =============================
    # REGISTER BLUEPRINTS
    # =============================

    from routes.main import main_bp

    app.register_blueprint(
        main_bp
    )


    from routes.shop import shop_bp

    app.register_blueprint(
        shop_bp
    )


    from routes.auth import auth_bp

    app.register_blueprint(
        auth_bp
    )


    from routes.cart import cart_bp

    app.register_blueprint(
        cart_bp
    )


    from routes.dashboard import dashboard_bp

    app.register_blueprint(
        dashboard_bp
    )


    from routes.checkout import checkout_bp

    app.register_blueprint(
        checkout_bp
    )


    from routes.orders import orders_bp

    app.register_blueprint(
        orders_bp
    )


    from routes.admin import admin_bp

    app.register_blueprint(
        admin_bp
    )


    from routes.messages import messages_bp

    app.register_blueprint(
        messages_bp
    )


    # =============================
    # CREATE DATABASE TABLES
    # =============================

    with app.app_context():

        db.create_all()


    return app


app = create_app()


if __name__ == "__main__":

    app.run()