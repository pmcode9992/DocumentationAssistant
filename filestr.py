import streamlit as st
import os

# def printDir(pth):
#     if os.path.isfile(pth):
#         st.write(pth)
#     else:
#         with st.sidebar:
#             with st.expander("📁" + pth):
#                 for i in os.listdir(pth):
#                     with st.container():  
#                         printDir(pth +"/" +i)


def printDir(pth):
    l=[]
    if os.path.isdir(pth):
        l = os.listdir(pth)
        for i in range(0, len(l)):
            if(os.path.isdir(pth + "/" + l[i])):
                l[i] = printDir((pth + "/" + l[i]))
    
    return {pth : l}
            
         
st.write("Welcome to DocuAssist")
# st.file_uploader("upload the root directory")

initial_path = st.text_input("Enter complete path of root directory")
if st.button("get file structure"):
    if not initial_path:
        st.error("Enter file path")
    else:
        os.chdir(initial_path)
        st.write(printDir(initial_path))
else:
    st.write("File structure here")

    