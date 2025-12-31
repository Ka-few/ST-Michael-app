from app.models import db, User
from werkzeug.security import generate_password_hash
import os


def create_admin():
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        print("⚠️ ADMIN_EMAIL or ADMIN_PASSWORD not set")
        return

    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        print("ℹ️ Admin already exists")
        return

    admin = User(
        name="Administrator",
        email=admin_email,
        role="admin",
        password=generate_password_hash(admin_password)
    )

    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user created")
