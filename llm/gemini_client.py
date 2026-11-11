import os

from dotenv import load_dotenv
from google import genai


# Load environment variables.
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


class GeminiClient:

    def __init__(self):

        if not API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Check your .env file."
            )

        self.client = genai.Client(
            api_key=API_KEY
        )

        # Gemini Flash model.
        self.model ="gemini-3.5-flash-lite"

        print("Gemini Client initialized!")

    def generate_response(self, prompt):

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            return response.text

        except Exception as error:

            print("Gemini API Error:", error)

            return None


if __name__ == "__main__":

    gemini = GeminiClient()

    response = gemini.generate_response(
        "You are ShopMind, an intelligent shopping assistant. "
        "Introduce yourself in two sentences."
    )

    print("\nGemini Response:\n")
    print(response)