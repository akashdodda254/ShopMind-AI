import re

from llm.gemini_client import GeminiClient


class ComparisonAgent:

    def __init__(self):
        self.gemini = GeminiClient()
        print("Comparison Agent initialized!")

    def compare(self, products):

        if len(products) < 2:
            return None

        cheapest = min(products, key=lambda p: p["price"])

        highest_rated = max(
            products,
            key=lambda p: p["rating"]
        )

        most_popular = max(
            products,
            key=lambda p: p["rating_count"]
        )

        return {
            "products": products,
            "cheapest": cheapest,
            "highest_rated": highest_rated,
            "most_popular": most_popular,
            "price_difference": (
                max(p["price"] for p in products)
                - min(p["price"] for p in products)
            )
        }

    def extract_specifications(self, product):

        specifications = product.get("specifications") or ""

        result = {}

        for item in specifications.split(";"):

            item = item.strip()

            if not item:
                continue

            parts = item.split(maxsplit=1)

            if len(parts) == 2:
                result[parts[1].strip().lower()] = parts[0].strip()
            else:
                result[item.lower()] = True

        return result

    def compare_specifications(self, products):

        return {
            product["name"]: self.extract_specifications(product)
            for product in products
        }

    def generate_ai_analysis(self, comparison):

        if not comparison:
            return "At least two products are required."

        products = comparison["products"]

        product_data = []

        for product in products:

            product_data.append({
                "name": product["name"],
                "brand": product["brand"],
                "price": product["price"],
                "rating": product["rating"],
                "reviews": product["rating_count"],
                "specifications": self.extract_specifications(product)
            })

        prompt = f"""
You are ShopMind, an intelligent shopping comparison assistant.

Compare these products using only the supplied information.

PRODUCTS:
{product_data}

Explain:
1. Which product offers the lowest price.
2. Which product has the highest rating.
3. Important specification differences.
4. Which product offers better value based on the available information.
5. Who should consider each product.

Rules:
- Never invent specifications.
- Never invent product features.
- Never change prices or ratings.
- Clearly mention when information is unavailable.
- Give a balanced recommendation.
- Keep the answer concise.
"""

        response = self.gemini.generate_response(prompt)

        if response:
            return response

        return self.format_comparison(comparison)

    def format_comparison(self, comparison):

        response = "PRODUCT COMPARISON\n"

        for product in comparison["products"]:

            response += (
                f"\n{product['name']}\n"
                f"Price: ₹{product['price']:,.0f}\n"
                f"Rating: {product['rating']}/5\n"
                f"Specifications: {product['specifications']}\n"
            )

        response += (
            f"\nLowest price: {comparison['cheapest']['name']}\n"
            f"Highest rating: {comparison['highest_rated']['name']}\n"
            f"Price difference: ₹{comparison['price_difference']:,.0f}\n"
        )

        return response