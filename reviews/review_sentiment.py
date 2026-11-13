import json
from llm.gemini_client import GeminiClient


class ReviewSentimentAnalyzer:

    def __init__(self):
        self.gemini = GeminiClient()

    def analyze_reviews(self, reviews):

        if not reviews:
            return []

        prompt = f"""
        Analyze the following customer product reviews.

        Classify each review as:
        - Positive
        - Negative
        - Neutral

        Return ONLY valid JSON in this format:

        [
            {{
                "review": "review text",
                "sentiment": "Positive",
                "reason": "short explanation"
            }}
        ]

        Do not invent information.

        Customer reviews:
        {json.dumps(reviews)}
        """

        response = self.gemini.generate_response(prompt)

        if not response:
            return []

        try:
            cleaned = response.strip()

            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
                cleaned = cleaned.rsplit("```", 1)[0]

            results = json.loads(cleaned)

            if not isinstance(results, list):
                return []

            return results

        except (json.JSONDecodeError, IndexError):
            return []

    def summarize_sentiment(self, results):

        summary = {
            "Positive": 0,
            "Negative": 0,
            "Neutral": 0
        }

        for item in results:
            sentiment = item.get("sentiment")

            if sentiment in summary:
                summary[sentiment] += 1

        return summary
