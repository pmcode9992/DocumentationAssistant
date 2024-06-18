import streamlit as st
import os
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

def genSummary(pth):
    summary = ""
    # code_snippet = ""
    # with open(pth, "r") as file:
    #     try:
    #         code_snippet = file.read()
    #         try: 
    #             summary = summarize_code(code_snippet)
    #             print(summary)
    #         except:
    #             return "Error summarising"
    #     except:
    #         return "Unreadable file"
    # # summary = summarize_code(code_snippet)
    return summary
    
def printDir(pth):
    l=[]
    if os.path.isdir(pth):
        l = os.listdir(pth)
        for i in range(0, len(l)):
            if(os.path.isdir(pth + "/" + l[i])):
                l[i] = printDir((pth + "/" + l[i]))
            else:
                l[i] = {(l[i]) : genSummary((pth + "/" + l[i]))}
    return {pth : l}

            
         
st.write("Welcome to DocuAssist")
# st.file_uploader("upload the root directory")

initial_path = st.text_input("Enter complete path of root directory")
if st.button("get file structure"):
    if not initial_path:
        st.error("Enter file path")
    else:
        os.chdir(initial_path)
        filestr = printDir(initial_path)
        st.write(filestr)
else:
    st.write("File structure here")

    