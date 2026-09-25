from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from extensions import db

from models.message import Message

from email_utils import send_email


main_bp = Blueprint(
    "main",
    __name__
)


# =============================
# ABOUT
# =============================

@main_bp.route("/about")
def about():

    return render_template(
        "about.html"
    )


# =============================
# CONTACT
# =============================

@main_bp.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact():

    if request.method == "POST":


        # =============================
        # GET FORM DATA
        # =============================

        name = request.form.get(
            "name"
        )

        email = request.form.get(
            "email"
        )

        phone = request.form.get(
            "phone"
        )

        message_text = request.form.get(
            "message"
        )


        # =============================
        # CHECK REQUIRED FIELDS
        # =============================

        if (
            not name
            or not email
            or not message_text
        ):

            flash(
                "Please fill in all required fields."
            )

            return redirect(
                url_for(
                    "main.contact"
                )
            )


        # =============================
        # CREATE MESSAGE
        # =============================

        message = Message(

            name=name,

            email=email,

            phone=phone,

            message=message_text

        )


        db.session.add(
            message
        )


        # =============================
        # SAVE MESSAGE
        # =============================

        try:

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            print(
                "CONTACT MESSAGE ERROR:",
                error
            )

            flash(
                "There was a problem sending your message. "
                "Please try again."
            )

            return redirect(
                url_for(
                    "main.contact"
                )
            )


        # =============================
        # EMAIL NOTIFICATION TO ADMIN
        # =============================

        admin_email = (
            "mwendasolomon464@gmail.com"
        )


        notification_subject = (
            "New Customer Message - FreshSip Juices"
        )


        notification_body = f"""You have received a new message from the FreshSip Juices website.

Customer Name:
{name}

Customer Email:
{email}

Customer Phone:
{phone if phone else "Not provided"}

Message:
{message_text}

Please log in to the FreshSip admin dashboard to view and reply to this message.
"""


        send_email(
            admin_email,
            notification_subject,
            notification_body
        )


        # =============================
        # SUCCESS
        # =============================

        flash(
            "Your message has been sent successfully. "
            "We will get back to you soon."
        )


        return redirect(
            url_for(
                "main.contact"
            )
        )


    return render_template(
        "contact.html"
    )