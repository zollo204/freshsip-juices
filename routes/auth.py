from flask import Blueprint, render_template, request, redirect, url_for, flash

from models.user import User

from extensions import db

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, logout_user


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")


        if not name or not email or not phone or not password:

            flash("Please fill in all fields.")

            return redirect(
                url_for("auth.register")
            )


        existing_email = User.query.filter_by(
            email=email
        ).first()


        if existing_email:

            flash(
                "An account with this email already exists."
            )

            return redirect(
                url_for("auth.register")
            )


        existing_phone = User.query.filter_by(
            phone=phone
        ).first()


        if existing_phone:

            flash(
                "An account with this phone number already exists."
            )

            return redirect(
                url_for("auth.register")
            )


        hashed_password = generate_password_hash(
            password
        )


        user = User(

            name=name,

            email=email,

            phone=phone,

            password=hashed_password,

            role="customer"

        )


        db.session.add(user)

        db.session.commit()


        flash(
            "Registration successful. You can now log in."
        )


        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "register.html"
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # FIND USER IN DATABASE

        user = User.query.filter_by(
            email=email
        ).first()

        # CHECK PASSWORD

        if user and check_password_hash(
            user.password,
            password
        ):

            # CHECK IF ACCOUNT IS DISABLED

            if not user.is_active:

                flash(
                    "Your account has been disabled. Please contact FreshSip support."
                )

                return redirect(
                    url_for("auth.login")
                )

            # LOG USER IN

            login_user(user)

            flash(
                "Login successful!"
            )

            # ADMIN LOGIN

            if user.role == "admin":

                return redirect(
                    url_for("admin.dashboard")
                )

            # CUSTOMER LOGIN

            return redirect(
                url_for("dashboard.dashboard")
            )

        # INVALID LOGIN

        flash(
            "Invalid email or password."
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "login.html"
    )

@auth_bp.route("/logout")
def logout():

    logout_user()


    flash(
        "You have been logged out."
    )


    return redirect(
        url_for("home")
    )