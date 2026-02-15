import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

print('Available Gemini Models:')
try:
    for m in genai.list_models():
        print(f"Model Name: {m.name}")
        print(f"  Methods: {m.supported_generation_methods}")
        print(f"  Display Name: {m.display_name}")
        print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
