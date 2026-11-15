import sqlite3
import bcrypt
import re
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "shopmind.db"


def create_users_table():

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def register_user(username, email, password):

    username = username.strip()
    email = email.strip().lower()

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Please enter a valid email address."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    try:

        with sqlite3.connect(DB_PATH) as connection:

            connection.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))

        return True, "Account created successfully!"

    except sqlite3.IntegrityError:

        return False, "Username or email already exists."


def login_user(email, password):

    email = email.strip().lower()

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        user = connection.execute("""
            SELECT id, username, email, password_hash
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

    if user is None:
        return None

    if bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"]
    ):

        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }

    return None


def get_user_by_id(user_id):

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        user = connection.execute("""
            SELECT id, username, email, created_at
            FROM users
            WHERE id = ?
        """, (user_id,)).fetchone()

    return dict(user) if user else None
def change_password(user_id, current_password, new_password):
    
    if len(new_password) < 8:
        return False, "New password must contain at least 8 characters."

    if current_password == new_password:
        return False, "New password must be different from your current password."

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        user = connection.execute(
            "SELECT password_hash FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if user is None:
            return False, "User account not found."

        if not bcrypt.checkpw(
            current_password.encode("utf-8"),
            user["password_hash"]
        ):
            return False, "Current password is incorrect."

        new_password_hash = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        )

        connection.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (new_password_hash, user_id)
        )

    return True, "Password changed successfully!"