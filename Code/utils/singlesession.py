
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import requests
import json
import copy
from utils.summariseChunks import sumChunks
from utils.gettokens import num_tokens_from_string
import langchain_openai

def getDocumentJSON_SHORT(filestr, length):
    code_file_extensions = [
    'py', 'js', 'java', 'cpp', 'c', 'html', 'css', 'php', 'rb', 'swift', 
    'cs', 'go', 'ts', 'jsx', 'tsx', 'scss', 'sass', 'less', 'json',
    ]
    filestr_copy = copy.deepcopy(filestr)
    
    if isinstance(filestr_copy, list):
        for i in range(len(filestr_copy)):
            filestr_copy[i] = getDocumentJSON_SHORT(filestr_copy[i], length)
    elif isinstance(filestr_copy, dict):
        for key, value in filestr_copy.items():
            if isinstance(value, str) and (key.split('.')[-1] in code_file_extensions):           
                filestr_copy[key] = getSummary(value, length)
            elif isinstance(value, str) and key.split('.')[-1] not in code_file_extensions:
                filestr_copy[key] = ""
            else:
                filestr_copy[key] = getDocumentJSON_SHORT(value, length)
    else:
        print(filestr_copy)
     
    return filestr_copy

def getDocumentJSON_LONG(filestr, shortSummary, length):
    code_file_extensions = [
    'py', 'js', 'java', 'cpp', 'c', 'html', 'css', 'php', 'rb', 'swift', 
    'cs', 'go', 'ts', 'jsx', 'tsx', 'scss', 'sass', 'less', 'json',
    ]
    filestr_copy = copy.deepcopy(filestr)
    
    if isinstance(filestr_copy, list):
        for i in range(len(filestr_copy)):
            filestr_copy[i] = getDocumentJSON_LONG(filestr_copy[i],shortSummary[i], length)
    elif isinstance(filestr_copy, dict):
        for key, value in filestr_copy.items():
            if isinstance(value, str) and (key.split('.')[-1] in code_file_extensions):           
                if num_tokens_from_string(value, "cl100k_base") < 750:
                    filestr_copy[key] = getSummary(value, length)
                else:
                    filestr_copy[key] = sumChunks(shortSummary[key], value, key.split('.')[-1])
                
            elif isinstance(value, str) and key.split('.')[-1] not in code_file_extensions:
                filestr_copy[key] = ""
            else:
                filestr_copy[key] = getDocumentJSON_LONG(value, shortSummary[key] , length)
    else:
        print(filestr_copy)
    
    return filestr_copy

def getSummary(codefile, length):
    
    load_dotenv()
    API_KEY = os.getenv("SingleSession_APIKEY")
    llm = ChatOpenAI(model="gpt-3.5-turbo",api_key = API_KEY) 
    if length == "long":
        prompt_template= """
        You are responsible for project documentation, in my project.Prepare documentation for this code as per guidelines. \nGuidelines \n- Markdown format \n- Include important code snippets if needed \n- explain the imports, and each of the functions\n Order of contents is brief explanation, imports, functionalities(with small code snippets 
        \n\n
        {codefile}
        """
    else:
        prompt_template = """
        You are responsible for project documentation, explain this code in very short\n\n
        {codefile}
        """
    prompt = PromptTemplate.from_template(prompt_template)
    llm_chain = prompt | llm
    response = llm_chain.invoke(codefile)
    return response.content
    
def getProjectSummary(context):
    load_dotenv()
    API_KEY = os.getenv("SingleSession_APIKEY")
    llm = ChatOpenAI(model="gpt-3.5-turbo",api_key = API_KEY) 
    prompt_template = """
        {context} + "\n\nYou are responsible for project documentation. Given short summaries of each codefile, from context. create an overall summary of the project, technologies used, what it's functionalities are."
    """
    prompt = PromptTemplate.from_template(prompt_template)
    llm_chain = prompt | llm
    response = llm_chain.invoke(str(context))
    return str(response.content)