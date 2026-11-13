from database.db import get_all_products
import math


class PersonalizedRecommendationEngine:

    def recommend(self, preferences, limit=5):
        products = get_all_products()
        scored_products = []

        categories = [
            item.lower()
            for item in preferences.get("categories", [])
        ]

        brands = [
            item.lower()
            for item in preferences.get("brands", [])
        ]

        keywords = [
            item.lower()
            for item in preferences.get("keywords", [])
        ]

        max_budget = preferences.get("max_budget")
        min_rating = preferences.get("min_rating", 0)

        max_reviews = max(
            (p["rating_count"] for p in products),
            default=1
        )

        for product in products:

            if product["stock"] <= 0:
                continue

            if max_budget is not None and product["price"] > max_budget:
                continue

            if product["rating"] < min_rating:
                continue

            score = (product["rating"] / 5) * 0.50

            popularity = (
                math.log1p(product["rating_count"])
                / math.log1p(max_reviews)
            )
            score += popularity * 0.20

            if product["category"].lower() in categories:
                score += 0.15

            if product["brand"].lower() in brands:
                score += 0.10

            product_text = (
                product["name"] + " " +
                product["description"] + " " +
                product["specifications"]
            ).lower()

            if any(word in product_text for word in keywords):
                score += 0.05

            scored_products.append({
                "product": product,
                "score": round(score, 4)
            })

        scored_products.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return scored_products[:limit]