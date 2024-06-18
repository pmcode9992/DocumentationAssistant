import google.generativeai as palm

def summarize_code(code_snippet):
    palm.configure(api_key="AIzaSyAzp_yFH6hiPx5RAgOsQXyYTdiMW8_6Abg")
    prompt = f"Summarize the following code:\n\n{code_snippet}\n\nSummary:"
    response = palm.generate_text(model="models/text-bison-001", prompt=prompt)
    
    if response and response.candidates:
        summary = response.candidates[0].get('output', 'No summary available').strip()
        return summary
    else:
        return "No summary available."


# if __name__ == "__main__":
    
#     code_snippet = ""
#     with open("./filestr.py", "r") as file:
#         code_snippet = file.read()
#     summary = summarize_code(code_snippet)
#     print("Summary:", summary)
