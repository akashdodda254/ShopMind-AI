from agents.intent_agent import IntentAgent
from agents.search_agent import SearchAgent
from agents.recommendation_agent import RecommendationAgent
from agents.comparison_agent import ComparisonAgent
from agents.response_agent import ResponseAgent


class ShopMindOrchestrator:

    def __init__(self):

        self.intent_agent = IntentAgent()
        self.search_agent = SearchAgent()
        self.recommendation_agent = RecommendationAgent()
        self.comparison_agent = ComparisonAgent()
        self.response_agent = ResponseAgent()

        print("ShopMind initialized successfully!")

    def process_request_data(
        self,
        message,
        category_override=None,
        budget_override=None
    ):

        message = message.strip()

        if not message:
            return {"type": "text", "response": "Please enter a shopping request."}

        if message.lower() in ["hi", "hello", "hey"]:
            return {
                "type": "text",
                "response": "Hello! Welcome to ShopMind. What are you shopping for today?"
            }

        requirements = self.intent_agent.understand(message)

        if requirements.get("intent") == "unknown":
            return {
                "type": "text",
                "response": "I couldn't understand your request. Please try again."
            }

        if category_override:
            requirements["category"] = category_override

        if budget_override is not None:
            requirements["max_price"] = budget_override

        products = self.search_agent.search(requirements)

        if not products:
            return {
                "type": "products",
                "products": [],
                "response": "No matching products found. Try changing your filters."
            }

        products = self.recommendation_agent.engine.rank_products(
            products
        )[:5]

        if requirements.get("intent") == "comparison":
            return {
                "type": "comparison",
                "products": products,
                "response": self.comparison_agent.compare(products)
            }

        response = self.response_agent.generate_response(products)

        return {
            "type": "products",
            "products": products,
            "response": response
        }

    def process_request(self, message):

        result = self.process_request_data(message)

        return result["response"]