"""Test de conexion a Gemini: lista los modelos disponibles para tu API key."""
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("Error: No se encontro GEMINI_API_KEY en el archivo .env")

client = genai.Client(api_key=api_key)

print("Modelos disponibles para tu llave:")
for model in client.models.list():
    print(f"- {model.name}")