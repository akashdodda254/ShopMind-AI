"""
ShopMind - Intelligent Product Search Engine

Features:
1. Category filtering
2. Budget filtering
3. Rating filtering
4. Keyword search
5. Product ranking
"""

from database.db import search_products


class RecommendationEngine:

    def __init__(self):

        print("ShopMind Recommendation Engine initialized!")

    # -----------------------------------------
    # SEARCH PRODUCTS
    # -----------------------------------------

    def search(
        self,
        keyword=None,
        category=None,
        min_price=None,
        max_price=None,
        min_rating=None,
        limit=10
    ):

        """
        Search products using customer requirements.
        """

        products = search_products(
            keyword=keyword,
            category=category,
            min_price=min_price,
            max_price=max_price,
            min_rating=min_rating
        )

        # Exclude unavailable products
        products = [
            product for product in products
            if product["stock"] > 0
        ]

        # Sort by rating and price
        products.sort(
            key=lambda product: (
                -product["rating"],
                product["price"]
            )
        )

        return products[:limit]

    # -----------------------------------------
    # RANK PRODUCTS
    # -----------------------------------------

    def rank_products(self, products):

        """
        Rank products using rating and review count.
        """

        if not products:
            return []

        def calculate_score(product):

            rating = product["rating"]

            review_count = product["rating_count"]

            # Logarithmic review weighting
            import math

            popularity = math.log1p(review_count)

            return (
                0.7 * rating +
                0.3 * popularity
            )

        ranked_products = sorted(
            products,
            key=calculate_score,
            reverse=True
        )

        return ranked_products

    # -----------------------------------------
    # GET RECOMMENDATIONS
    # -----------------------------------------

    def recommend(
        self,
        category=None,
        max_price=None,
        min_rating=0,
        keyword=None,
        limit=5
    ):

        """
        Return personalized product recommendations.
        """

        products = self.search(
            keyword=keyword,
            category=category,
            max_price=max_price,
            min_rating=min_rating,
            limit=100
        )

        ranked_products = self.rank_products(products)

        return ranked_products[:limit]


# ---------------------------------------------
# MANUAL TEST
# ---------------------------------------------

if __name__ == "__main__":

    engine = RecommendationEngine()

    print("\nSearching for gaming laptops under ₹75,000...\n")

    results = engine.recommend(
        category="Laptop",
        max_price=75000,
        min_rating=4.3,
        keyword="gaming",
        limit=5
    )

    for index, product in enumerate(results, start=1):

        print(f"\nRecommendation {index}")

        print(f"Name: {product['name']}")

        print(f"Brand: {product['brand']}")

        print(f"Price: ₹{product['price']:,.0f}")

        print(f"Rating: {product['rating']}/5")

        print(f"Reviews: {product['rating_count']}")

        print(f"Stock: {product['stock']}")