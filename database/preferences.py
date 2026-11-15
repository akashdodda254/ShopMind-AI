import sqlite3
import json
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "shopmind.db"


def create_preferences_table():

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                categories TEXT DEFAULT '[]',
                brands TEXT DEFAULT '[]',
                keywords TEXT DEFAULT '[]',
                max_budget REAL,
                min_rating REAL DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)


def save_preferences(user_id, preferences):

    create_preferences_table()

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute("""
            INSERT INTO user_preferences (
                user_id,
                categories,
                brands,
                keywords,
                max_budget,
                min_rating,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)

            ON CONFLICT(user_id)
            DO UPDATE SET
                categories = excluded.categories,
                brands = excluded.brands,
                keywords = excluded.keywords,
                max_budget = excluded.max_budget,
                min_rating = excluded.min_rating,
                updated_at = CURRENT_TIMESTAMP
        """, (
            user_id,
            json.dumps(preferences.get("categories", [])),
            json.dumps(preferences.get("brands", [])),
            json.dumps(preferences.get("keywords", [])),
            preferences.get("max_budget"),
            preferences.get("min_rating", 0)
        ))

    return True


def get_preferences(user_id):

    create_preferences_table()

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        result = connection.execute("""
            SELECT *
            FROM user_preferences
            WHERE user_id = ?
        """, (user_id,)).fetchone()

    if not result:
        return {
            "categories": [],
            "brands": [],
            "keywords": [],
            "max_budget": None,
            "min_rating": 0
        }

    return {
        "categories": json.loads(result["categories"]),
        "brands": json.loads(result["brands"]),
        "keywords": json.loads(result["keywords"]),
        "max_budget": result["max_budget"],
        "min_rating": result["min_rating"]
    }