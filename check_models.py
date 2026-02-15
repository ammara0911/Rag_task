import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Try alternate env var
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: API Key not found in environment.")
else:
    genai.configure(api_key=api_key)
    try:
        print("Listing models to file...")
        with open("available_models.txt", "w") as f:
            for m in genai.list_models():
                f.write(f"Model: {m.name}\n")
                f.write(f"  Methods: {m.supported_generation_methods}\n")
        print("Done.")
    except Exception as e:
        print(f"Error listing models: {e}")
