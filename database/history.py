import sqlite3
import json
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "shopmind.db"


def initialize_history_table():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS shopping_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            query TEXT NOT NULL,
            category TEXT,
            budget REAL,
            product_ids TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def record_search(
    query,
    category=None,
    budget=None,
    products=None,
    user_id="guest"
):
    products = products or []

    product_ids = [
        product["id"]
        for product in products
        if product.get("id") is not None
    ]

    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        INSERT INTO shopping_history
        (user_id, query, category, budget, product_ids)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        query,
        category,
        budget,
        json.dumps(product_ids)
    ))

    connection.commit()
    connection.close()


def get_recent_searches(user_id="guest", limit=10):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    rows = connection.execute("""
        SELECT *
        FROM shopping_history
        WHERE user_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()

    connection.close()

    return [dict(row) for row in rows]

def learn_preferences(user_id="guest"):
    history = get_recent_searches(user_id=user_id, limit=50)

    category_counts = {}
    keywords = []

    for search in history:
        category = search.get("category")

        if category:
            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

        words = search["query"].lower().split()
        keywords.extend(words)

    preferred_categories = sorted(
        category_counts,
        key=category_counts.get,
        reverse=True
    )

    ignored_words = {
        "find", "recommend", "show", "me", "best",
        "under", "with", "for", "the", "a", "an"
    }

    keyword_counts = {}

    for word in keywords:
        word = word.strip(".,!?")

        if len(word) > 2 and word not in ignored_words:
            keyword_counts[word] = keyword_counts.get(word, 0) + 1

    preferred_keywords = sorted(
        keyword_counts,
        key=keyword_counts.get,
        reverse=True
    )[:5]

    return {
        "categories": preferred_categories[:3],
        "keywords": preferred_keywords
    }
