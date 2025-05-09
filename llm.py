import os
from dotenv import load_dotenv
import google.generativeai as genai

def generate_gemini_response(prompt: str) -> str:
    # Load environment variables
    load_dotenv()

    # Fetch API key and model name
    api_key = os.getenv("API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not api_key or not model_name:
        raise ValueError("API_KEY or MODEL_NAME not found in .env file.")

    # Configure GenAI
    genai.configure(api_key=api_key)

    # Initialize model
    model = genai.GenerativeModel(model_name)

    # Generate response
    response = model.generate_content(prompt)
    return response.text

# Example usage
if __name__ == "__main__":
    print(generate_gemini_response("Write a haiku about the moon."))
