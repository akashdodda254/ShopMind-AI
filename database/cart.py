import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "shopmind.db"


def create_cart_table():

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS shopping_cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(user_id, product_id),

                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)


def add_to_cart(user_id, product_id, quantity=1):

    if quantity < 1:
        return False, "Quantity must be at least 1."

    create_cart_table()

    with sqlite3.connect(DB_PATH) as connection:

        product = connection.execute(
            "SELECT id, stock FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()

        if not product:
            return False, "Product not found."

        existing = connection.execute("""
            SELECT quantity
            FROM shopping_cart
            WHERE user_id = ? AND product_id = ?
        """, (user_id, product_id)).fetchone()

        new_quantity = quantity + (existing[0] if existing else 0)

        if new_quantity > product[1]:
            return False, "Requested quantity exceeds available stock."

        connection.execute("""
            INSERT INTO shopping_cart (user_id, product_id, quantity)
            VALUES (?, ?, ?)

            ON CONFLICT(user_id, product_id)
            DO UPDATE SET quantity = excluded.quantity
        """, (user_id, product_id, new_quantity))

    return True, "Product added to your cart!"


def get_cart(user_id):

    create_cart_table()

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        results = connection.execute("""
            SELECT
                p.*,
                c.quantity,
                c.added_at AS cart_added_at,
                (p.price * c.quantity) AS subtotal

            FROM shopping_cart c

            JOIN products p
                ON c.product_id = p.id

            WHERE c.user_id = ?

            ORDER BY c.added_at DESC
        """, (user_id,)).fetchall()

    return [dict(row) for row in results]


def update_cart_quantity(user_id, product_id, quantity):

    if quantity < 1:
        return False, "Quantity must be at least 1."

    with sqlite3.connect(DB_PATH) as connection:

        product = connection.execute(
            "SELECT stock FROM products WHERE id = ?",
            (product_id,)
        ).fetchone()

        if not product:
            return False, "Product not found."

        if quantity > product[0]:
            return False, "Requested quantity exceeds available stock."

        cursor = connection.execute("""
            UPDATE shopping_cart
            SET quantity = ?
            WHERE user_id = ? AND product_id = ?
        """, (quantity, user_id, product_id))

    if cursor.rowcount:
        return True, "Cart quantity updated."

    return False, "Cart item not found."


def remove_from_cart(user_id, product_id):

    with sqlite3.connect(DB_PATH) as connection:

        cursor = connection.execute("""
            DELETE FROM shopping_cart
            WHERE user_id = ? AND product_id = ?
        """, (user_id, product_id))

    if cursor.rowcount:
        return True, "Product removed from cart."

    return False, "Product not found in cart."


def clear_cart(user_id):

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            DELETE FROM shopping_cart
            WHERE user_id = ?
        """, (user_id,))

    return True, "Shopping cart cleared."


def get_cart_total(user_id):

    cart_items = get_cart(user_id)

    return sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )