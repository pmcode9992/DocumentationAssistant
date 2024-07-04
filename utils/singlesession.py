
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json
import copy


def getDocumentJSON(filestr, length):
    code_file_extensions = [
    'py', 'js', 'java', 'cpp', 'c', 'html', 'css', 'php', 'rb', 'swift', 
    'cs', 'go', 'ts', 'jsx', 'tsx', 'scss', 'sass', 'less', 'json',
    ]
    filestr_copy = copy.deepcopy(filestr)
    
    if isinstance(filestr_copy, list):
        for i in range(len(filestr_copy)):
            filestr_copy[i] = getDocumentJSON(filestr_copy[i], length)
    elif isinstance(filestr_copy, dict):
        for key, value in filestr_copy.items():
            if isinstance(value, str) and (key.split('.')[-1] in code_file_extensions):
                filestr_copy[key] = getSummary(value, length)
            elif isinstance(value, str) and key.split('.')[-1] not in code_file_extensions:
                filestr_copy[key] = "Not a code file"
            else:
                filestr_copy[key] = getDocumentJSON(value, length)
    else:
        print(filestr_copy)
    
    return filestr_copy


def getSummary(codefile, length):
    
    load_dotenv()
    API_KEY = os.getenv("SingleSession_APIKEY")
    API_URL = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    client = OpenAI(
    organization='org-kf9It3OCjQvnf6UtiL9lJLQx',
    project='proj_mlnucjj9ruxVKvFjDAdgHIKP',
    api_key= API_KEY
    )
   
    if length == "long":
        data = {
            "model" : "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": ("You are responsible for project documentation, in my project.Prepare brief documentation for this code" + codefile)}],
            "temperature": 0.7,
        }
    else:
        data = {
            "model" : "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": ("Explain this code in very short.\n" + codefile)}],
            "temperature": 0.7,
        }
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
        
    else:
        return f"Error: {response.status_code}, {response.text}"

def getProjectSummary(context):
    
    load_dotenv()
    API_KEY = os.getenv("SingleSession_APIKEY")
    API_URL = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    client = OpenAI(
    organization='org-kf9It3OCjQvnf6UtiL9lJLQx',
    project='proj_mlnucjj9ruxVKvFjDAdgHIKP',
    api_key= API_KEY
    )
    data = {
        "model" : "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": (str(context) + "\n\nYou are responsible for project documentation. Given short summaries of each codefile, from context. create an overall summary of the project, technologies used, what it's functionalities are.")}],
        "temperature": 0.7,
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
        
    else:
        return f"Error: {response.status_code}, {response.text}"

    
    
# def getSummary(code, length):
#     if length == "short":
#         return "Short summary"
#     else:
#         return "Long summary"


    
    
    
