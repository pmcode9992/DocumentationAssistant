
import streamlit as st
import os
from dotenv import load_dotenv
# import google.generativeai as palm
import concurrent.futures
from io import StringIO
import tiktoken
from utils.singlesession import getDocumentJSON, getProjectSummary
from utils.gettokens import num_tokens_from_string
from utils.projectstr import getProjectStructure, getFolderStructure
from utils.genPDF import genratePDF

load_dotenv()
key = os.getenv("api")
contextWindow = int(os.getenv("contextWindow"))

# def summarize_code(code_snippet):
#     palm.configure(api_key=key)
#     prompt = f"Summarize the following code:\n\n{code_snippet}\n\nSummary:"
#     response = palm.generate_text(model="models/text-bison-001", prompt=prompt)
    
#     if response and response.candidates:
#         summary = response.candidates[0].get('output', 'No summary available').strip()
#         return summary
#     else:
#         return "No summary available."

filestr = None
totalTokens = None

if "shortSum" not in st.session_state:
    st.session_state["shortSum"] = None
if "longSum" not in st.session_state:
    st.session_state["longSum"] = None
if "projSum" not in st.session_state:
    st.session_state["projSum"] = None
if "get_file_structure" not in st.session_state:
    st.session_state["get_file_structure"] = False
if "generate_doc" not in st.session_state:
    st.session_state["generate_doc"] = False

st.write("Welcome to DocuAssist")

initial_path = st.text_input("Enter complete path of root directory")

docuIgnore = st.radio("I would like to :",
            ["Upload docuignore file", "List out files to be ignored", "Auto generate docuignore"],
            captions = ["Similar to .gitignore, specify which files and directories should be ignored and not tracked. It helps prevent certain files, like temporary files, build artifacts, and sensitive information, from being included in the documentation.","learn more : https://www.w3schools.com/git/git_ignore.asp?remote=github","Use AI to get list of files to be ignored"], index=1, disabled=True)

if docuIgnore == "Upload docuignore file":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)
        unwantedFiles = stringio.read()
        st.write(unwantedFiles)

elif docuIgnore == "List out files to be ignored":
    unwantedFiles = st.text_area("Enter file/folder names to be ignored",
                        "node_modules\n" 
                        ".env\n" 
                        ".gitignore\n")
    st.write(unwantedFiles)

if (st.button("get file structure") or st.session_state["get_file_structure"]) and docuIgnore:
    st.session_state["get_file_structure"] = True
    if not initial_path:
        st.error("Enter file path")
    else:
        # if docuIgnore == "Auto generate docuignore":
        #     os.chdir(initial_path)
        #     unwantedFiles = ["Banana\nBread"]
        #     projectStr = getProjectStructure(initial_path, unwantedFiles)
            
        unwantedFilesList = unwantedFiles.split()
        
        os.chdir(initial_path)
        filestr = getProjectStructure(initial_path, unwantedFilesList)
        foldrstr = getFolderStructure(initial_path, unwantedFilesList)
        
        st.write("Your Project structure")
        st.write(filestr)
        st.write("Files/Folders to be ignored - ")
        st.write(unwantedFilesList)
        
        totalTokens = num_tokens_from_string(str(filestr), "cl100k_base")
        st.write("Total number of tokens in file structure  - " + str(totalTokens))



if st.button("Generate Document") and st.session_state["get_file_structure"]:   
    st.session_state["generate_doc"] = True   
    shortSummary = getDocumentJSON(filestr, "short")
    longSummary = getDocumentJSON(filestr, "long")
    projSummary = None
    if totalTokens < contextWindow * 0.9:
        projSummary = getProjectSummary(filestr)
    else:
        projSummary = getProjectSummary(shortSummary)
    st.write(projSummary)
    st.write("Short Summaries")
    st.write(shortSummary)
    st.write("Long Summaries")
    st.write(longSummary)
    
    
    st.session_state["shortSum"] = shortSummary
    st.session_state["longSum"] = longSummary
    st.session_state["projSum"] = projSummary

# if st.button("Download PDF") and st.session_state["generate_doc"] and (st.session_state["projSum"] and st.session_state["longSum"]):
#     # st.write(st.session_state["projSum"])
#     # st.write(st.session_state["shortSum"])
#     # st.write(st.session_state["longSum"])
#     st.write("⏳ Making your pdf")
    
#     genratePDF("Signature Scribbles",foldrstr, st.session_state["projSum"], st.session_state["longSum"])
    
    
    
        #THREADS (to be updated)
        # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        #     list_ofpaths = [os.path.join(initial_path, f) for f in os.listdir(initial_path) if os.path.isfile(os.path.join(initial_path, f))]
        #     future_to_summary = {executor.submit(genSummary, pth): pth for pth in list_ofpaths}
        #     for future in concurrent.futures.as_completed(future_to_summary):
        #         summary_result = future_to_summary[future]
        #         try:
        #             summary = future.result()
        #             print(f"Summary for {summary_result}: {summary}")
        #         except Exception as exc:
        #             print(f"Error processing {summary_result}: {exc}")
            
