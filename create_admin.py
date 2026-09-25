from app import app

from extensions import db

from models.user import User

from werkzeug.security import generate_password_hash


with app.app_context():

    admin = User(
        name="FreshSip Admin",
        email="admin@freshsip.com",
        phone="0700000000",
        password=generate_password_hash("Admin@123"),
        role="admin"
    )

    db.session.add(admin)

    db.session.commit()

    print("Admin account created successfully!")