from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


def get_response(code, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+code)
    return response.text


def get_summary(file_name):
    with open(file_name, 'r') as file:
        code = file.read()

    prompt = f"Summarize the following code:\n\n{code}"
    summary = get_response(code, prompt)
    return summary

file_path = "/Users/rejonasusan/Desktop/HPE/DocumentationAssistant/main.py"
summary = get_summary(file_path)
print(summary)