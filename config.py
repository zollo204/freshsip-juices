import os

from dotenv import load_dotenv


load_dotenv()


class Config:


    # =============================
    # APPLICATION
    # =============================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "freshsip-development-key"
    )


    # =============================
    # DATABASE
    # =============================

    SQLALCHEMY_DATABASE_URI = "sqlite:///freshsip.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # =============================
    # MPESA
    # =============================

    MPESA_PAYBILL = os.getenv(
        "MPESA_PAYBILL"
    )

    MPESA_ACCOUNT = os.getenv(
        "MPESA_ACCOUNT"
    )


    # =============================
    # EMAIL SETTINGS
    # =============================

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER"
    )

    MAIL_PORT = int(
        os.getenv(
            "MAIL_PORT",
            587
        )
    )

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    MAIL_USE_TLS = os.getenv(
        "MAIL_USE_TLS",
        "True"
    ).lower() == "true"

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER"
    )