class ComparisonAgent:
    
    def __init__(self):
        print("Comparison Agent initialized!")

    def compare(self, products):

        if len(products) < 2:
            return "At least two products are needed for comparison."

        response = "\nPRODUCT COMPARISON\n"
        response += "=" * 60 + "\n"

        for index, product in enumerate(products, start=1):

            response += (
                f"\nProduct {index}: {product['name']}\n"
                f"Brand: {product['brand']}\n"
                f"Price: ₹{product['price']:,.0f}\n"
                f"Rating: {product['rating']}/5\n"
                f"Reviews: {product['rating_count']}\n"
                f"Stock: {product['stock']}\n"
                f"Specifications: {product['specifications']}\n"
            )

            response += "-" * 60 + "\n"

        cheapest = min(products, key=lambda p: p["price"])
        highest_rated = max(products, key=lambda p: p["rating"])

        response += (
            f"\nLowest price: {cheapest['name']}\n"
            f"Highest rating: {highest_rated['name']}\n"
        )

        return response