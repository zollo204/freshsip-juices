from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db

from models.message import Message

from email_utils import send_email


messages_bp = Blueprint(
    "messages",
    __name__,
    url_prefix="/admin/messages"
)


# =============================
# ADMIN CHECK
# =============================

def admin_required():

    return (
        current_user.is_authenticated
        and current_user.role == "admin"
    )


# =============================
# ALL MESSAGES
# =============================

@messages_bp.route("/")
@login_required
def messages():

    if not admin_required():

        return "Unauthorized", 403


    customer_messages = Message.query.order_by(
        Message.created_at.desc()
    ).all()


    unread_count = Message.query.filter_by(
        status="Unread"
    ).count()


    return render_template(
        "admin/messages.html",
        messages=customer_messages,
        unread_count=unread_count
    )


# =============================
# VIEW MESSAGE
# =============================

@messages_bp.route(
    "/view/<int:message_id>"
)
@login_required
def view_message(message_id):

    if not admin_required():

        return "Unauthorized", 403


    message = Message.query.get_or_404(
        message_id
    )


    # Automatically mark unread message as read

    if message.status == "Unread":

        message.status = "Read"

        db.session.commit()


    return render_template(
        "admin/message_detail.html",
        message=message
    )


# =============================
# MARK MESSAGE AS READ
# =============================

@messages_bp.route(
    "/read/<int:message_id>"
)
@login_required
def mark_read(message_id):

    if not admin_required():

        return "Unauthorized", 403


    message = Message.query.get_or_404(
        message_id
    )


    message.status = "Read"

    db.session.commit()


    flash(
        "Message marked as read."
    )


    return redirect(
        url_for(
            "messages.messages"
        )
    )


# =============================
# REPLY TO CUSTOMER
# =============================

@messages_bp.route(
    "/reply/<int:message_id>",
    methods=["POST"]
)
@login_required
def reply_message(message_id):

    if not admin_required():

        return "Unauthorized", 403


    message = Message.query.get_or_404(
        message_id
    )


    reply_text = request.form.get(
        "reply",
        ""
    ).strip()


    if not reply_text:

        flash(
            "Please enter a reply."
        )

        return redirect(
            url_for(
                "messages.view_message",
                message_id=message.id
            )
        )


    subject = (
        "Re: Your message to FreshSip Juices"
    )


    body = f"""Hello {message.name},

Thank you for contacting FreshSip Juices.

{reply_text}

Kind regards,

FreshSip Juices
Fresh, Natural & Healthy Juices
"""


    sent = send_email(
        message.email,
        subject,
        body
    )


    if sent:

        message.status = "Replied"

        db.session.commit()


        flash(
            "Your reply has been sent successfully."
        )

    else:

        flash(
            "The reply could not be sent. "
            "Please check your email settings."
        )


    return redirect(
        url_for(
            "messages.view_message",
            message_id=message.id
        )
    )


# =============================
# DELETE MESSAGE
# =============================

@messages_bp.route(
    "/delete/<int:message_id>",
    methods=["POST"]
)
@login_required
def delete_message(message_id):

    if not admin_required():

        return "Unauthorized", 403


    message = Message.query.get_or_404(
        message_id
    )


    db.session.delete(
        message
    )

    db.session.commit()


    flash(
        "Message deleted successfully."
    )


    return redirect(
        url_for(
            "messages.messages"
        )
    )