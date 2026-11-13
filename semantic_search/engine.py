import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from database.db import get_all_products


class SemanticSearchEngine:

    def __init__(self):

        print("Loading semantic search model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.products = []
        self.product_embeddings = None

        self.load_product_embeddings()

        print("Semantic Search Engine initialized!")

    def load_product_embeddings(self):

        self.products = get_all_products()

        if not self.products:
            self.product_embeddings = None
            return

        descriptions = []

        for product in self.products:

            text = (
                f"{product['name']}. "
                f"Brand: {product['brand']}. "
                f"Category: {product['category']}. "
                f"Description: {product['description']}. "
                f"Specifications: {product['specifications']}."
            )

            descriptions.append(text)

        self.product_embeddings = self.model.encode(
            descriptions,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def search(
        self,
        query,
        category=None,
        max_price=None,
        limit=5
    ):

        if self.product_embeddings is None:
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        similarities = cosine_similarity(
            query_embedding,
            self.product_embeddings
        )[0]

        results = []

        for index, product in enumerate(self.products):

            if product["stock"] <= 0:
                continue

            if category and product["category"].lower() != category.lower():
                continue

            if max_price is not None and product["price"] > max_price:
                continue

            results.append({
                "product": product,
                "similarity": float(similarities[index])
            })

        results.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

        return results[:limit]


if __name__ == "__main__":

    engine = SemanticSearchEngine()

    query = "Laptop suitable for gaming and performance"

    results = engine.search(query)

    print("\nSemantic Search Results:\n")

    for result in results:

        product = result["product"]

        print(f"\nProduct: {product['name']}")
        print(f"Price: ₹{product['price']:,.0f}")
        print(f"Similarity: {result['similarity']:.4f}")