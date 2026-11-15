from database.db import get_connection


def advanced_search_products(
    keyword=None,
    category=None,
    brand=None,
    min_price=None,
    max_price=None,
    min_rating=None,
    sort_by="relevance",
    in_stock_only=False,
    limit=50,
    offset=0
):
    """
    Advanced product search for ShopMind.

    Supports:
    - Keyword search
    - Category filtering
    - Brand filtering
    - Price range
    - Minimum rating
    - Specification search
    - Stock filtering
    - Multiple sorting options
    - Pagination
    """

    if min_price is not None and min_price < 0:
        raise ValueError("Minimum price cannot be negative.")

    if max_price is not None and max_price < 0:
        raise ValueError("Maximum price cannot be negative.")

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise ValueError(
            "Minimum price cannot exceed maximum price."
        )

    if min_rating is not None and not 0 <= min_rating <= 5:
        raise ValueError("Rating must be between 0 and 5.")

    allowed_sort_options = {
        "relevance": "rating DESC, rating_count DESC",
        "price_low": "price ASC",
        "price_high": "price DESC",
        "rating": "rating DESC, rating_count DESC",
        "popularity": "rating_count DESC, rating DESC",
        "newest": "created_at DESC"
    }

    if sort_by not in allowed_sort_options:
        raise ValueError("Invalid sorting option.")

    limit = max(1, min(int(limit), 100))
    offset = max(0, int(offset))

    connection = get_connection()

    try:

        query = """
            SELECT *
            FROM products
            WHERE 1=1
        """

        parameters = []

        # Keyword search
        if keyword and keyword.strip():

            search_term = f"%{keyword.strip()}%"

            query += """
                AND (
                    name LIKE ?
                    OR brand LIKE ?
                    OR description LIKE ?
                    OR specifications LIKE ?
                )
            """

            parameters.extend([
                search_term,
                search_term,
                search_term,
                search_term
            ])

        # Category filter
        if category:
            query += " AND category = ?"
            parameters.append(category)

        # Brand filter
        if brand:
            query += " AND brand = ?"
            parameters.append(brand)

        # Minimum price
        if min_price is not None:
            query += " AND price >= ?"
            parameters.append(min_price)

        # Maximum price
        if max_price is not None:
            query += " AND price <= ?"
            parameters.append(max_price)

        # Minimum rating
        if min_rating is not None:
            query += " AND rating >= ?"
            parameters.append(min_rating)

        # Stock filter
        if in_stock_only:
            query += " AND stock > 0"

        # Sorting
        query += f" ORDER BY {allowed_sort_options[sort_by]}"

        # Pagination
        query += " LIMIT ? OFFSET ?"

        parameters.extend([limit, offset])

        cursor = connection.cursor()

        cursor.execute(query, parameters)

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()


def get_product_filter_options():
    """
    Retrieve available categories and brands
    for search filters.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT DISTINCT category
            FROM products
            WHERE category IS NOT NULL
            ORDER BY category
        """)

        categories = [
            row["category"]
            for row in cursor.fetchall()
        ]

        cursor.execute("""
            SELECT DISTINCT brand
            FROM products
            WHERE brand IS NOT NULL
            ORDER BY brand
        """)

        brands = [
            row["brand"]
            for row in cursor.fetchall()
        ]

        return {
            "categories": categories,
            "brands": brands
        }

    finally:
        connection.close()