import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as palm
import concurrent.futures


load_dotenv()
key = os.getenv("api")

def summarize_code(code_snippet):
    palm.configure(api_key=key)
    prompt = f"Summarize the following code:\n\n{code_snippet}\n\nSummary:"
    response = palm.generate_text(model="models/text-bison-001", prompt=prompt)
    
    if response and response.candidates:
        summary = response.candidates[0].get('output', 'No summary available').strip()
        return summary
    else:
        return "No summary available."

def genSummary(pth):
    summary = ""
    code_snippet = ""
    with open(pth, "r") as file:
        try:
            code_snippet = file.read()
            try: 
                summary = summarize_code(code_snippet)
            except:
                return "Error summarising"
        except:
            return "Unreadable file"
    return summary
    
def printDir(pth):
    l=[]
    unwanted_files = ["Node Modules", ".DS_Store", "__pycache__", "docuAssist", "DA", ".git", ".env", ".gitignore", ".gitattributes"]
    if os.path.isdir(pth):
        l = os.listdir(pth)
        l = list(filter(lambda x : x not in unwanted_files, l))
        for i in range(0, len(l)):
            if(os.path.isdir(pth + "/" + l[i])):
                l[i] = printDir((pth + "/" + l[i]))
            else:
                l[i] = {(l[i]) : genSummary((pth + "/" + l[i]))}
    return {pth : l}
         
st.write("Welcome to DocuAssist")

initial_path = st.text_input("Enter complete path of root directory")
if st.button("get file structure"):
    if not initial_path:
        st.error("Enter file path")
    else:
        os.chdir(initial_path)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            list_ofpaths = [os.path.join(initial_path, f) for f in os.listdir(initial_path) if os.path.isfile(os.path.join(initial_path, f))]
            future_to_summary = {executor.submit(genSummary, pth): pth for pth in list_ofpaths}
            for future in concurrent.futures.as_completed(future_to_summary):
                summary_result = future_to_summary[future]
                try:
                    summary = future.result()
                    print(f"Summary for {summary_result}: {summary}")
                except Exception as exc:
                    print(f"Error processing {summary_result}: {exc}")

        filestr = printDir(initial_path)
        st.write(filestr)
else:
    st.write("File structure here")

    