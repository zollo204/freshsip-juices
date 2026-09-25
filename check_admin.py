from app import app

from models.user import User


with app.app_context():

    user = User.query.filter_by(
        email="admin@freshsip.com"
    ).first()


    if user:

        print("Admin account found.")

        print("Name:", user.name)

        print("Email:", user.email)

        print("Role:", user.role)

    else:

        print("Admin account was NOT found.")