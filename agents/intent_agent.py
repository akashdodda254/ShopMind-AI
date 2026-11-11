import json

from llm.gemini_client import GeminiClient


class IntentAgent:

    def __init__(self):
        self.gemini = GeminiClient()
        print("Gemini-powered Intent Agent initialized!")

    def understand(self, message):

        prompt = f"""
You are the intent detection system for ShopMind.

Extract shopping requirements from the customer message.

Return ONLY valid JSON with these fields:
{{
    "intent": "product_search",
    "category": null,
    "max_price": null,
    "min_rating": 0,
    "keyword": null,
    "preferences": []
}}

Allowed categories:
Laptop, Smartphone, Headphones, Smartwatch.

Allowed intents:
product_search, recommendation, comparison.

Rules:
- Extract the maximum budget as a number in INR.
- Extract minimum rating between 0 and 5.
- Put product features and use cases in keyword.
- Put additional requirements in preferences.
- Do not invent missing information.
- Return JSON only.

Customer message: {message}
"""

        response = self.gemini.generate_response(prompt)

        if not response:
            return {
                "intent": "unknown"
            }

        try:
            cleaned = response.strip()

            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "")

            requirements = json.loads(cleaned)

            return requirements

        except (json.JSONDecodeError, TypeError):
            print("Gemini returned invalid JSON.")
            return {"intent": "unknown"}