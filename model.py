from dotenv import load_dotenv
from google.generativeai import genai
import os

load_dotenv()

api = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key = api)