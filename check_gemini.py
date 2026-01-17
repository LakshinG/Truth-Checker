import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Create the new 2026 Client
client = genai.Client(api_key=api_key)

try:
    # Testing with the current standard model
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents="Hello"
    )
    print(f"SUCCESS: Gemini replied: {response.text}")
except Exception as e:
    print(f"FAILED: Google says: {e}")