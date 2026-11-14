import sqlite3
from pathlib import Path


DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "shopmind.db"
)


class PriceTracker:

    def __init__(self):
        self.create_table()

    def create_table(self):
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    price REAL NOT NULL,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def record_price(self, product_id, price):
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute("""
                INSERT INTO price_history (product_id, price)
                VALUES (?, ?)
            """, (product_id, price))

    def get_price_history(self, product_id):
        with sqlite3.connect(DB_PATH) as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute("""
                SELECT price, recorded_at
                FROM price_history
                WHERE product_id = ?
                ORDER BY recorded_at ASC, id ASC
            """, (product_id,)).fetchall()

        return [dict(row) for row in rows]

    def compare_prices(self, product_id, current_price):
        history = self.get_price_history(product_id)

        if not history:
            return {
                "current_price": current_price,
                "previous_price": None,
                "change": None,
                "message": "No previous price data available."
            }

        previous_price = history[-1]["price"]
        change = current_price - previous_price

        if change < 0:
            message = f"Price decreased by ₹{abs(change):,.2f}"
        elif change > 0:
            message = f"Price increased by ₹{change:,.2f}"
        else:
            message = "Price has not changed."

        return {
            "current_price": current_price,
            "previous_price": previous_price,
            "change": change,
            "message": message
        }

    def check_price_drop(self, product_id, current_price):
        history = self.get_price_history(product_id)

        if not history:
            return {
                "alert": False,
                "message": "No previous price available."
            }

        previous_price = history[-1]["price"]

        if current_price < previous_price:
            difference = previous_price - current_price
            percentage = (difference / previous_price) * 100

            return {
                "alert": True,
                "previous_price": previous_price,
                "current_price": current_price,
                "difference": difference,
                "percentage": round(percentage, 2),
                "message": (
                    f"Price dropped by ₹{difference:,.2f} "
                    f"({percentage:.2f}%)!"
                )
            }

        return {
            "alert": False,
            "message": "No price drop detected."
        }
