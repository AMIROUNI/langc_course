from dotenv import load_dotenv
import requests
import os
load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OLLAMA_API_KEY")

if not api_key:
    raise ValueError("OLLAMA_API_KEY not found in .env") 


response = requests.get(
    "https://ollama.com/api/tags",
    headers={
        "Authorization": f"Bearer {api_key}"
    },
    timeout=30
)


data = response.json() 

print("\nOllama Cloud models:\n")
response.raise_for_status()
for model in data.get("models", []):
    print(f"Model: {model.get('name')}")
    print("-" * 40)