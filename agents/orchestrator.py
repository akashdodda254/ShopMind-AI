from agents.intent_agent import IntentAgent
from agents.search_agent import SearchAgent
from agents.recommendation_agent import RecommendationAgent
from agents.comparison_agent import ComparisonAgent
from agents.response_agent import ResponseAgent


class ShopMindOrchestrator:

    def __init__(self):

        print("\nInitializing ShopMind AI...\n")

        self.intent_agent = IntentAgent()
        self.search_agent = SearchAgent()
        self.recommendation_agent = RecommendationAgent()
        self.comparison_agent = ComparisonAgent()
        self.response_agent = ResponseAgent()

        print("\nShopMind is ready!\n")

    def process_request(self, message):

        message = message.strip()

        if not message:
            return "Please enter a shopping request."

        if message.lower() in ["hi", "hello", "hey"]:
            return "Hello! Welcome to ShopMind. What are you shopping for today?"

        if message.lower() in ["bye", "exit", "quit"]:
            return "Thank you for shopping with ShopMind!"

        # 1. Understand the request using Gemini.
        try:
            requirements = self.intent_agent.understand(message)
        except Exception as error:
            print("Intent Agent error:", error)
            return "I'm having trouble understanding your request. Please try again."

        if requirements.get("intent") == "unknown":
            return "I couldn't understand your request. Please describe the product you need."

        # 2. Search the product database.
        search_results = self.search_agent.search(requirements)

        if not search_results:
            return "No matching products found. Try changing your budget or preferences."

        # 3. Rank matching products.
        recommendations = self.recommendation_agent.engine.rank_products(
            search_results
        )[:5]

        # 4. Compare when requested.
        if requirements.get("intent") == "comparison":
            return self.comparison_agent.compare(recommendations)

        # 5. Generate the final response using Gemini.
        try:
            return self.response_agent.generate_response(recommendations)
        except Exception as error:
            print("Response Agent error:", error)
            return self.response_agent.format_fallback(recommendations)


if __name__ == "__main__":

    shopmind = ShopMindOrchestrator()

    print("===================================")
    print("       SHOPMIND AI ASSISTANT")
    print("===================================")
    print("Type 'exit' to quit.\n")

    while True:

        message = input("You: ").strip()

        if message.lower() in ["exit", "quit", "bye"]:
            print("\nShopMind: Thank you for shopping!")
            break

        response = shopmind.process_request(message)

        print("\nShopMind:\n")
        print(response)
        print()