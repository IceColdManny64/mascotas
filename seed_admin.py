"""Create initial admin user if not exists."""
import os
import sys

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.user import User, UserRole

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@mascotas.local")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin12345")
ADMIN_NAME = os.environ.get("ADMIN_NAME", "Administrador")


def main():
    app = create_app()
    with app.app_context():
        if User.query.filter_by(email=ADMIN_EMAIL).first():
            print(f"Admin already exists: {ADMIN_EMAIL}")
            return
        user = User(
            email=ADMIN_EMAIL,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            name=ADMIN_NAME,
            role=UserRole.admin,
        )
        db.session.add(user)
        db.session.commit()
        print(f"Admin created: {ADMIN_EMAIL}")


if __name__ == "__main__":
    main()
    sys.exit(0)
