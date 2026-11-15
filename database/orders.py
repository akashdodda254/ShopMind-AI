import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "shopmind.db"


def create_orders_tables():

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'Placed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                subtotal REAL NOT NULL,

                FOREIGN KEY (order_id)
                    REFERENCES orders(id),

                FOREIGN KEY (product_id)
                    REFERENCES products(id)
            )
        """)


def place_order(user_id):

    create_orders_tables()

    try:
        with sqlite3.connect(DB_PATH) as connection:

            connection.execute("PRAGMA foreign_keys = ON")

            cart_items = connection.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price,
                    p.stock,
                    c.quantity

                FROM shopping_cart c

                JOIN products p
                    ON c.product_id = p.id

                WHERE c.user_id = ?
            """, (user_id,)).fetchall()

            if not cart_items:
                return False, "Your shopping cart is empty."

            total_amount = 0

            for product_id, name, price, stock, quantity in cart_items:

                if quantity > stock:
                    return False, f"Insufficient stock for {name}."

                total_amount += price * quantity

            cursor = connection.execute("""
                INSERT INTO orders (user_id, total_amount, status)
                VALUES (?, ?, 'Placed')
            """, (user_id, total_amount))

            order_id = cursor.lastrowid

            for product_id, name, price, stock, quantity in cart_items:

                connection.execute("""
                    INSERT INTO order_items (
                        order_id,
                        product_id,
                        product_name,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    order_id,
                    product_id,
                    name,
                    quantity,
                    price,
                    price * quantity
                ))

            connection.execute("""
                DELETE FROM shopping_cart
                WHERE user_id = ?
            """, (user_id,))

            return True, {
                "order_id": order_id,
                "total_amount": total_amount
            }

    except sqlite3.Error as error:

        return False, f"Unable to place order: {error}"


def get_user_orders(user_id):

    create_orders_tables()

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        results = connection.execute("""
            SELECT *
            FROM orders
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,)).fetchall()

    return [dict(row) for row in results]


def get_order_details(order_id, user_id):

    create_orders_tables()

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        order = connection.execute("""
            SELECT *
            FROM orders
            WHERE id = ? AND user_id = ?
        """, (order_id, user_id)).fetchone()

        if not order:
            return None

        items = connection.execute("""
            SELECT *
            FROM order_items
            WHERE order_id = ?
        """, (order_id,)).fetchall()

    return {
        "order": dict(order),
        "items": [dict(item) for item in items]
    }


def update_order_status(order_id, user_id, new_status):

    allowed_statuses = [
        "Placed",
        "Processing",
        "Shipped",
        "Delivered",
        "Cancelled",
    ]

    if new_status not in allowed_statuses:
        return False, "Invalid order status."

    with sqlite3.connect(DB_PATH) as connection:

        cursor = connection.execute("""
            UPDATE orders
            SET status = ?
            WHERE id = ? AND user_id = ?
        """, (new_status, order_id, user_id))

    if cursor.rowcount:
        return True, "Order status updated."

    return False, "Order not found."
def cancel_order(order_id, user_id):
    
    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("PRAGMA foreign_keys = ON")

        order = connection.execute("""
            SELECT status
            FROM orders
            WHERE id = ? AND user_id = ?
        """, (order_id, user_id)).fetchone()

        if not order:
            return False, "Order not found."

        if order[0] != "Placed":
            return False, (
                "This order can no longer be cancelled. "
                "Only orders with Placed status can be cancelled."
            )

        connection.execute("""
            UPDATE orders
            SET status = 'Cancelled'
            WHERE id = ? AND user_id = ?
        """, (order_id, user_id))

    return True, "Your order has been cancelled successfully."