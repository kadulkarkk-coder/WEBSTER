from aura.config.api_keys import APIKeys

keys = APIKeys()

print(keys.get("gemini"))
print(keys.get("claude"))
print(keys.get("openai"))