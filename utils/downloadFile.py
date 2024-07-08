import base64
import streamlit as st

def download_markdown_file(markdown_text, file_name):
    # Convert markdown text to bytes
    markdown_bytes = markdown_text.encode('utf-8')
    
    # Create a link for downloading the file
    b64 = base64.b64encode(markdown_bytes).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{file_name}">Download .md file</a>'
    st.markdown(href, unsafe_allow_html=True)
