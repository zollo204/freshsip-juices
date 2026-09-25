import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import current_app


def send_email(
    recipient,
    subject,
    body
):

    mail_server = current_app.config.get(
        "MAIL_SERVER"
    )

    mail_port = current_app.config.get(
        "MAIL_PORT"
    )

    username = current_app.config.get(
        "MAIL_USERNAME"
    )

    password = current_app.config.get(
        "MAIL_PASSWORD"
    )

    sender = current_app.config.get(
        "MAIL_DEFAULT_SENDER"
    )

    use_tls = current_app.config.get(
        "MAIL_USE_TLS",
        True
    )


    if not mail_server or not username or not password:

        print(
            "EMAIL ERROR: Email settings are not configured."
        )

        return False


    message = MIMEMultipart()

    message["From"] = sender or username

    message["To"] = recipient

    message["Subject"] = subject


    message.attach(
        MIMEText(
            body,
            "plain"
        )
    )


    try:

        server = smtplib.SMTP(
            mail_server,
            mail_port
        )

        server.ehlo()


        if use_tls:

            server.starttls()

            server.ehlo()


        server.login(
            username,
            password
        )


        server.sendmail(
            sender or username,
            recipient,
            message.as_string()
        )


        server.quit()


        return True


    except Exception as error:

        print(
            "EMAIL ERROR:",
            error
        )

        return False