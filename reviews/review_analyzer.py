from database.db import get_all_products


class ReviewAnalyzer:

    def analyze_product(self, product):
        rating = product.get("rating", 0)
        review_count = product.get("rating_count", 0)

        if rating >= 4.5:
            rating_status = "Excellent"
        elif rating >= 4.0:
            rating_status = "Very Good"
        elif rating >= 3.0:
            rating_status = "Average"
        else:
            rating_status = "Needs Improvement"

        if review_count >= 1000:
            popularity = "Very Popular"
        elif review_count >= 300:
            popularity = "Popular"
        else:
            popularity = "Limited Review Data"

        return {
            "name": product["name"],
            "rating": rating,
            "review_count": review_count,
            "rating_status": rating_status,
            "popularity": popularity
        }

    def analyze_all_products(self):
        products = get_all_products()

        results = [
            self.analyze_product(product)
            for product in products
        ]

        return sorted(
            results,
            key=lambda item: (
                item["rating"],
                item["review_count"]
            ),
            reverse=True
        )

    def get_top_rated_products(self, limit=5):
        return self.analyze_all_products()[:limit]
