"""
ShopMind - AI Shopping Assistant

Features:
1. Understand basic shopping requests
2. Extract product categories
3. Extract maximum budget
4. Extract minimum rating
5. Search products
6. Recommend matching products
"""

import re

from recommendation.engine import RecommendationEngine


class ShoppingAssistant:

    def __init__(self):
        self.engine = RecommendationEngine()

        self.categories = [
            "Laptop",
            "Smartphone",
            "Headphones",
            "Smartwatch"
        ]

        print("ShopMind Shopping Assistant is ready!")

    def extract_budget(self, message):
        """
        Extract maximum budget from a message.

        Examples:
        under 75000
        below 50000
        less than 1 lakh
        under 75k
        """

        patterns = [
            r"(?:under|below|less than|within|budget of|maximum|upto|up to)\s*₹?\s*(\d+(?:\.\d+)?)\s*(lakh|lakhs|k)?",
            r"₹\s*(\d+(?:\.\d+)?)\s*(lakh|lakhs|k)?"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                message,
                re.IGNORECASE
            )

            if match:

                amount = float(match.group(1))
                unit = (match.group(2) or "").lower()

                if unit in ["lakh", "lakhs"]:
                    amount *= 100000

                elif unit == "k":
                    amount *= 1000

                return int(amount)

        return None

    def extract_rating(self, message):
        """
        Extract minimum rating.

        Example:
        rating above 4.3
        at least 4.5 stars
        """

        patterns = [
            r"(?:above|over|greater than|at least|minimum|minimum rating of)\s*(\d(?:\.\d+)?)\s*(?:stars?|rating)?",
            r"rating(?: of)?\s*(\d(?:\.\d+)?)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                message,
                re.IGNORECASE
            )

            if match:
                rating = float(match.group(1))

                if 0 <= rating <= 5:
                    return rating

        return 0

    def extract_category(self, message):

        message_lower = message.lower()

        for category in self.categories:

            if category.lower() in message_lower:
                return category

        # Handle common variations.
        if "phone" in message_lower:
            return "Smartphone"

        if "headphone" in message_lower:
            return "Headphones"

        if "watch" in message_lower:
            return "Smartwatch"

        return None

    def extract_keyword(self, message, category):
        """
        Remove budget, rating and category phrases
        to identify useful product search keywords.
        """

        keyword = message.lower()

        # Remove budget expressions.
        keyword = re.sub(
            r"(?:under|below|less than|within|budget of|maximum|upto|up to)\s*₹?\s*\d+(?:\.\d+)?\s*(?:lakh|lakhs|k)?",
            "",
            keyword
        )

        keyword = re.sub(
            r"₹\s*\d+(?:\.\d+)?\s*(?:lakh|lakhs|k)?",
            "",
            keyword
        )

        # Remove rating expressions.
        keyword = re.sub(
            r"(?:above|over|greater than|at least|minimum|minimum rating of)\s*\d(?:\.\d+)?\s*(?:stars?|rating)?",
            "",
            keyword
        )

        keyword = re.sub(
            r"rating(?: of)?\s*\d(?:\.\d+)?",
            "",
            keyword
        )

        # Remove category.
        if category:
            keyword = re.sub(
                re.escape(category.lower()),
                "",
                keyword
            )

        # Remove conversational words.
        stop_words = [
            "find", "me", "show", "recommend",
            "suggest", "some", "good", "best",
            "i", "want", "need", "a", "an",
            "the", "for", "with", "and",
            "products", "product", "please",
            "buy", "looking", "search"
        ]

        words = keyword.split()

        useful_words = [
            word for word in words
            if word not in stop_words
        ]

        return " ".join(useful_words).strip() or None

    def understand_request(self, message):

        category = self.extract_category(message)

        budget = self.extract_budget(message)

        rating = self.extract_rating(message)

        keyword = self.extract_keyword(
            message,
            category
        )

        return {
            "category": category,
            "max_price": budget,
            "min_rating": rating,
            "keyword": keyword
        }

    def search_products(self, requirements):

        return self.engine.recommend(
            category=requirements["category"],
            max_price=requirements["max_price"],
            min_rating=requirements["min_rating"],
            keyword=requirements["keyword"],
            limit=5
        )

    def format_recommendations(self, products):

        if not products:
            return (
                "I couldn't find matching products. "
                "Try changing your budget or search terms."
            )

        response = "\nHere are my recommendations:\n"

        for index, product in enumerate(products, start=1):

            response += (
                f"\n{index}. {product['name']}\n"
                f"   Brand: {product['brand']}\n"
                f"   Price: ₹{product['price']:,.0f}\n"
                f"   Rating: {product['rating']}/5\n"
                f"   Reviews: {product['rating_count']}\n"
                f"   Stock: {product['stock']}\n"
            )

        return response

    def chat(self, message):

        message = message.strip()

        if not message:
            return "Please enter a shopping request."

        message_lower = message.lower()

        if message_lower in ["hi", "hello", "hey"]:
            return (
                "Hello! Welcome to ShopMind.\n"
                "Tell me what product you're looking for "
                "and your budget."
            )

        if message_lower in ["exit", "quit", "bye"]:
            return "Thank you for using ShopMind!"

        requirements = self.understand_request(message)

        products = self.search_products(requirements)

        return self.format_recommendations(products)


if __name__ == "__main__":

    assistant = ShoppingAssistant()

    print("\n================================")
    print("       SHOPMIND ASSISTANT")
    print("================================")
    print("Ask me to find products.")
    print("Type 'exit' to quit.\n")

    while True:

        user_message = input("You: ")

        if user_message.lower().strip() in [
            "exit", "quit", "bye"
        ]:
            print("\nShopMind: Thank you for shopping with us!")
            break

        response = assistant.chat(user_message)

        print("\nShopMind:", response)