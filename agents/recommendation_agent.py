from recommendation.engine import RecommendationEngine


class RecommendationAgent:

    def __init__(self):
        self.engine = RecommendationEngine()
        print("Recommendation Agent initialized!")

    def recommend(self, requirements):

        products = self.engine.search(
            keyword=requirements.get("keyword"),
            category=requirements.get("category"),
            max_price=requirements.get("max_price"),
            min_rating=requirements.get("min_rating"),
            limit=100
        )

        ranked_products = self.engine.rank_products(products)

        return ranked_products[:5]