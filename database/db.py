"""
ShopMind - Product Database Module

Handles:
1. SQLite database connections
2. Product table creation
3. Product insertion
4. Product retrieval
5. Product searching
"""

import sqlite3
from pathlib import Path


# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DATABASE_PATH = BASE_DIR / "database" / "shopmind.db"


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():
    """
    Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: Database connection
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # Return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# --------------------------------------------------
# CREATE PRODUCTS TABLE
# --------------------------------------------------

def create_tables():
    """
    Create the products table if it does not exist.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                brand TEXT NOT NULL,

                category TEXT NOT NULL,

                price REAL NOT NULL CHECK(price >= 0),

                rating REAL DEFAULT 0
                    CHECK(rating >= 0 AND rating <= 5),

                rating_count INTEGER DEFAULT 0
                    CHECK(rating_count >= 0),

                description TEXT,

                specifications TEXT,

                stock INTEGER DEFAULT 0
                    CHECK(stock >= 0),

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Indexes improve common search operations
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_category
            ON products(category)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_price
            ON products(price)
        """)

        connection.commit()

        print("Products table created successfully!")

    finally:
        connection.close()


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

def initialize_database():
    """
    Initialize the ShopMind database.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    create_tables()

    print("ShopMind database initialized successfully!")


# --------------------------------------------------
# ADD SINGLE PRODUCT
# --------------------------------------------------

def add_product(
    name,
    brand,
    category,
    price,
    rating=0,
    rating_count=0,
    description="",
    specifications="",
    stock=0
):
    """
    Insert a single product into the database.

    Returns:
        int: ID of the inserted product.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO products (
                name,
                brand,
                category,
                price,
                rating,
                rating_count,
                description,
                specifications,
                stock
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            brand,
            category,
            price,
            rating,
            rating_count,
            description,
            specifications,
            stock
        ))

        connection.commit()

        product_id = cursor.lastrowid

        print(f"Product added successfully! ID: {product_id}")

        return product_id

    finally:
        connection.close()


# --------------------------------------------------
# ADD MULTIPLE PRODUCTS
# --------------------------------------------------

def add_products(products):
    """
    Insert multiple products into the database.

    Args:
        products (list): List of product dictionaries.

    Returns:
        int: Number of inserted products.
    """

    if not products:
        return 0

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO products (
                name,
                brand,
                category,
                price,
                rating,
                rating_count,
                description,
                specifications,
                stock
            )
            VALUES (
                :name,
                :brand,
                :category,
                :price,
                :rating,
                :rating_count,
                :description,
                :specifications,
                :stock
            )
        """

        cursor.executemany(query, products)

        connection.commit()

        print(f"{cursor.rowcount} products added successfully!")

        return cursor.rowcount

    finally:
        connection.close()


# --------------------------------------------------
# GET ALL PRODUCTS
# --------------------------------------------------

def get_all_products():
    """
    Retrieve all products.

    Returns:
        list: List of product records.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM products
            ORDER BY id
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# --------------------------------------------------
# GET PRODUCT BY ID
# --------------------------------------------------

def get_product_by_id(product_id):
    """
    Retrieve a product using its ID.

    Returns:
        dict or None: Product information.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM products
            WHERE id = ?
        """, (product_id,))

        result = cursor.fetchone()

        return dict(result) if result else None

    finally:
        connection.close()


# --------------------------------------------------
# SEARCH PRODUCTS
# --------------------------------------------------

def search_products(
    keyword=None,
    category=None,
    min_price=None,
    max_price=None,
    min_rating=None
):
    """
    Search products using multiple filters.

    All filters are optional.

    Returns:
        list: Matching products.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = "SELECT * FROM products WHERE 1=1"

        parameters = []

        if keyword:

            query += """
                AND (
                    name LIKE ?
                    OR brand LIKE ?
                    OR description LIKE ?
                )
            """

            search_term = f"%{keyword}%"

            parameters.extend([
                search_term,
                search_term,
                search_term
            ])

        if category:

            query += " AND category = ?"

            parameters.append(category)

        if min_price is not None:

            query += " AND price >= ?"

            parameters.append(min_price)

        if max_price is not None:

            query += " AND price <= ?"

            parameters.append(max_price)

        if min_rating is not None:

            query += " AND rating >= ?"

            parameters.append(min_rating)

        query += " ORDER BY rating DESC, price ASC"

        cursor.execute(query, parameters)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# --------------------------------------------------
# RUN DATABASE INITIALIZATION
# --------------------------------------------------

if __name__ == "__main__":

    initialize_database()