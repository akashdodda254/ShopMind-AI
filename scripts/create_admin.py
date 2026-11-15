import sqlite3
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from database.admin import make_user_admin

DB_PATH = PROJECT_ROOT / "database" / "shopmind.db"


def create_first_admin():

    print("\n🛡️ ShopMind Administrator Setup")
    print("-" * 40)

    email = input("Enter your registered ShopMind email: ").strip().lower()

    if not email:
        print("Email cannot be empty.")
        return

    with sqlite3.connect(DB_PATH) as connection:

        user = connection.execute(
            """
            SELECT id, username, email
            FROM users
            WHERE LOWER(email) = ?
            """,
            (email,),
        ).fetchone()

    if not user:
        print("No registered account found with that email.")
        return

    user_id, username, registered_email = user

    print(f"\nAccount found: {username}")
    print(f"Email: {registered_email}")

    confirmation = input(
        "\nGrant administrator privileges to this account? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Administrator setup cancelled.")
        return

    success, message = make_user_admin(user_id)

    if success:
        print(f"\n✅ {message}")
        print("You can now access the ShopMind Admin Dashboard.")
    else:
        print(f"\n❌ {message}")


if __name__ == "__main__":
    create_first_admin()