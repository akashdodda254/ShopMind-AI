import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "shopmind.db"


def initialize_admin_database():

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS admin_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)


def make_user_admin(user_id):

    initialize_admin_database()

    with sqlite3.connect(DB_PATH) as connection:

        user = connection.execute(
            "SELECT id FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if not user:
            return False, "User does not exist."

        connection.execute("""
            INSERT OR IGNORE INTO admin_settings (user_id)
            VALUES (?)
        """, (user_id,))

    return True, "Administrator access granted."


def is_admin(user_id):

    initialize_admin_database()

    with sqlite3.connect(DB_PATH) as connection:

        result = connection.execute("""
            SELECT 1
            FROM admin_settings
            WHERE user_id = ?
        """, (user_id,)).fetchone()

    return result is not None


def get_dashboard_stats(admin_id):

    if not is_admin(admin_id):
        raise PermissionError("Administrator access required.")

    with sqlite3.connect(DB_PATH) as connection:

        total_users = connection.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        total_products = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        total_orders = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

        total_revenue = connection.execute("""
            SELECT COALESCE(SUM(total_amount), 0)
            FROM orders
            WHERE status != 'Cancelled'
        """).fetchone()[0]

        pending_orders = connection.execute("""
            SELECT COUNT(*)
            FROM orders
            WHERE status = 'Placed'
        """).fetchone()[0]

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
    }


def get_all_users(admin_id):

    if not is_admin(admin_id):
        raise PermissionError("Administrator access required.")

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        users = connection.execute("""
            SELECT id, username, email, created_at
            FROM users
            ORDER BY created_at DESC
        """).fetchall()

    return [dict(user) for user in users]


def get_all_orders(admin_id):

    if not is_admin(admin_id):
        raise PermissionError("Administrator access required.")

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        orders = connection.execute("""
            SELECT
                o.id,
                o.user_id,
                u.username,
                o.total_amount,
                o.status,
                o.created_at
            FROM orders o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.created_at DESC
        """).fetchall()

    return [dict(order) for order in orders]


def admin_update_order_status(admin_id, order_id, new_status):

    if not is_admin(admin_id):
        raise PermissionError("Administrator access required.")

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
            WHERE id = ?
        """, (new_status, order_id))

    if cursor.rowcount:
        return True, "Order status updated successfully."

    return False, "Order not found."


def get_inventory(admin_id):

    if not is_admin(admin_id):
        raise PermissionError("Administrator access required.")

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        products = connection.execute("""
            SELECT
                id,
                name,
                brand,
                category,
                price,
                stock
            FROM products
            ORDER BY stock ASC
        """).fetchall()

    return [dict(product) for product in products]