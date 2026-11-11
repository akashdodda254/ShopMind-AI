from llm.gemini_client import GeminiClient


class ResponseAgent:

    def __init__(self):
        self.gemini = GeminiClient()
        print("Gemini Response Agent initialized!")

    def generate_response(self, products):

        if not products:
            return "No matching products found."

        # Only provide actual database information to Gemini.
        product_data = []

        for product in products:
            product_data.append({
                "name": product["name"],
                "brand": product["brand"],
                "price": product["price"],
                "rating": product["rating"],
                "reviews": product["rating_count"],
                "stock": product["stock"],
                "specifications": product["specifications"]
            })

        prompt = f"""
You are ShopMind, an intelligent shopping assistant.

Explain these product recommendations to the customer.

PRODUCT DATA:
{product_data}

Instructions:
1. Explain why these products may be useful.
2. Highlight price and rating.
3. Compare important specifications when relevant.
4. Never invent product features.
5. Never change prices or ratings.
6. Keep the response concise and helpful.
7. Mention that recommendations are based on available catalogue data.
"""

        response = self.gemini.generate_response(prompt)

        if response:
            return response

        # Fallback if Gemini is unavailable.
        return self.format_fallback(products)

    def format_fallback(self, products):

        response = "Here are your recommendations:\n"

        for index, product in enumerate(products, start=1):

            response += (
                f"\n{index}. {product['name']}\n"
                f"Brand: {product['brand']}\n"
                f"Price: ₹{product['price']:,.0f}\n"
                f"Rating: {product['rating']}/5\n"
            )

        return response