from app.database import SessionLocal
from app.models import Admin
from app.core.security import hash_password
from getpass import getpass


def create_admin():
    db = SessionLocal()

    print("\n=== Create Admin User ===")

    email = input("Admin email: ").strip()
    full_name = input("Full name: ").strip()

    if not email:
        print("Email cannot be empty!")
        return

    # Check if admin exists
    existing = db.query(Admin).filter(Admin.email == email).first()
    if existing:
        print("Admin already exists with this email!")
        return

    while True:
        password = getpass("Password: ")
        confirm = getpass("Confirm password: ")

        if not password:
            print("Password cannot be empty!")
            continue

        if password != confirm:
            print("Passwords do not match! Try again.\n")
            continue

        break  # both password fields are OK

    new_admin = Admin(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password)
    )

    db.add(new_admin)
    db.commit()

    print("\nAdmin created successfully!")
    print(f"Email: {email}")
    print("You can now log in as admin.\n")


if __name__ == "__main__":
    create_admin()
