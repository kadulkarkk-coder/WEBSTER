from aura.config.api_keys import APIKeys

keys = APIKeys()

print(keys.get("gemini"))
print(keys.get("claude"))
print(keys.get("openai"))

from google import genai

API_KEY = "AQ.Ab8RN6LXA5WrX0deejaPxWHSPlxSPz7jUxlT1utoHuH7jucFDg"

client = genai.Client(
    api_key=API_KEY
)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Reply with only: Hello WEBSTER!"
)

print(response.text)