import unittest

from agents.shopping_assistant import ShoppingAssistant


class TestShoppingAssistant(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assistant = ShoppingAssistant()

    def test_extract_budget(self):

        budget = self.assistant.extract_budget(
            "Find a laptop under 75000"
        )

        self.assertEqual(budget, 75000)

    def test_extract_budget_in_lakhs(self):

        budget = self.assistant.extract_budget(
            "Find a laptop under 1 lakh"
        )

        self.assertEqual(budget, 100000)

    def test_extract_budget_in_thousands(self):

        budget = self.assistant.extract_budget(
            "Find a laptop under 75k"
        )

        self.assertEqual(budget, 75000)

    def test_extract_category(self):

        category = self.assistant.extract_category(
            "I need a smartphone"
        )

        self.assertEqual(category, "Smartphone")

    def test_extract_rating(self):

        rating = self.assistant.extract_rating(
            "Show laptops above 4.3 rating"
        )

        self.assertEqual(rating, 4.3)

    def test_understand_request(self):

        result = self.assistant.understand_request(
            "Find gaming laptops under 75000"
        )

        self.assertEqual(result["category"], "Laptop")
        self.assertEqual(result["max_price"], 75000)
        self.assertIn("gaming", result["keyword"])

    def test_empty_message(self):

        result = self.assistant.chat("")

        self.assertEqual(
            result,
            "Please enter a shopping request."
        )


if __name__ == "__main__":
    unittest.main()