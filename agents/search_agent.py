from recommendation.engine import RecommendationEngine


class SearchAgent:

    def __init__(self):
        self.engine = RecommendationEngine()
        print("Search Agent initialized!")

    def search(self, requirements):

        return self.engine.search(
            keyword=requirements.get("keyword"),
            category=requirements.get("category"),
            max_price=requirements.get("max_price"),
            min_rating=requirements.get("min_rating"),
            limit=100
        )