from app import app
from extensions import db
from models import User

with app.app_context():
    admin = User(
        username="ywenchen",
        email="ywenchen@school.com",
        first_name="Yi",
        last_name="Wen Chen",
        role="student"
    )
    admin.set_password("password")
    db.session.add(admin)
    db.session.commit()
    print("Admin created!")