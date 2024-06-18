import google.generativeai as palm
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

key = os.getenv("api")

palm.configure(api_key=key)

def summarize_code(code_snippet):
    prompt = f"Summarize the following code:\n\n{code_snippet}\n\nSummary:"
    response = palm.generate_text(model="models/text-bison-001", prompt=prompt)
    
    if response and response.candidates:
        summary = response.candidates[0].get('output', 'No summary available').strip()
        return summary
    else:
        return "No summary available."
    

def main():

    st.title("Code summarization")
    st.write("Give code here: ")

    code = st.text_area("Code Snippet", height=300)

    if st.button("Summarize"):
        if not code.strip():
            st.error("Please enter a code snippet to summarize.")
        else:
            with st.spinner("Summarizing..."):
                summary = summarize_code(code)
            st.subheader("Summary")
            st.write(summary)



if __name__ == "__main__":
    main()
