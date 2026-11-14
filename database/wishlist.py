import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "shopmind.db"


def create_wishlist_table():

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS wishlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, product_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)


def add_to_wishlist(user_id, product_id):

    create_wishlist_table()

    try:
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute("""
                INSERT INTO wishlist (user_id, product_id)
                VALUES (?, ?)
            """, (user_id, product_id))

        return True, "Product added to your wishlist!"

    except sqlite3.IntegrityError:
        return False, "This product is already in your wishlist."


def remove_from_wishlist(user_id, product_id):

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute("""
            DELETE FROM wishlist
            WHERE user_id = ? AND product_id = ?
        """, (user_id, product_id))

    if cursor.rowcount:
        return True, "Product removed from your wishlist."

    return False, "Product was not found in your wishlist."


def get_wishlist(user_id):

    create_wishlist_table()

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        results = connection.execute("""
            SELECT
                p.*,
                w.added_at AS wishlist_added_at
            FROM wishlist w
            JOIN products p ON w.product_id = p.id
            WHERE w.user_id = ?
            ORDER BY w.added_at DESC
        """, (user_id,)).fetchall()

    return [dict(row) for row in results]


def is_in_wishlist(user_id, product_id):

    create_wishlist_table()

    with sqlite3.connect(DB_PATH) as connection:
        result = connection.execute("""
            SELECT 1
            FROM wishlist
            WHERE user_id = ? AND product_id = ?
        """, (user_id, product_id)).fetchone()

    return result is not None