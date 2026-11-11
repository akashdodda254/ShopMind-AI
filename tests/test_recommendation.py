import unittest

from recommendation.engine import RecommendationEngine


class TestRecommendationEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.engine = RecommendationEngine()

    def test_budget_filter(self):

        results = self.engine.recommend(
            category="Laptop",
            max_price=75000,
            limit=10
        )

        for product in results:

            self.assertLessEqual(
                product["price"],
                75000
            )

    def test_rating_filter(self):

        results = self.engine.recommend(
            category="Laptop",
            min_rating=4.3,
            limit=10
        )

        for product in results:

            self.assertGreaterEqual(
                product["rating"],
                4.3
            )

    def test_category_filter(self):

        results = self.engine.recommend(
            category="Smartphone",
            limit=10
        )

        for product in results:

            self.assertEqual(
                product["category"],
                "Smartphone"
            )

    def test_empty_results(self):

        results = self.engine.recommend(
            category="Laptop",
            max_price=1000
        )

        self.assertEqual(results, [])


if __name__ == "__main__":

    unittest.main()