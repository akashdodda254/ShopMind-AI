from recommendation.engine import RecommendationEngine
from semantic_search.engine import SemanticSearchEngine


class SearchAgent:

    def __init__(self):

        self.engine = RecommendationEngine()
        self.semantic_engine = SemanticSearchEngine()

        print("Search Agent initialized!")

    def search(self, requirements):

        keyword = requirements.get("keyword")
        category = requirements.get("category")
        max_price = requirements.get("max_price")
        min_rating = requirements.get("min_rating", 0)

        # Use semantic search when a meaningful keyword exists.
        if keyword:

            results = self.semantic_engine.search(
                query=keyword,
                category=category,
                max_price=max_price,
                limit=100
            )

            products = [
                item["product"]
                for item in results
                if item["product"]["rating"] >= min_rating
            ]

            if products:
                return self.engine.rank_products(products)

        # Fallback to traditional database search.
        return self.engine.search(
            keyword=keyword,
            category=category,
            max_price=max_price,
            min_rating=min_rating,
            limit=100
        )