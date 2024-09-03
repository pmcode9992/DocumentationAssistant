from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from utils.textSplit import getChunks

load_dotenv()
API_KEY = os.getenv("SingleSession_APIKEY")

def sumChunks(shortSummary, code, lang):
    splits = getChunks(code, lang)
    chunks = [shortSummary]
    for i in splits:
        chunks.append(i.page_content)
    

    llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=API_KEY) 

    prompt_template = """You are an expert programmer responsible for preparing documentation for a large codefile, You will have an array containing summary of the entire code file in the 0th index, followed by summaries of the chunks of files encountered so far. Your task is to understand the context and generate an explanation for the next chunk of code.\n\n
    Output Format(Markdown)- \n
    (for imports) \n
    ### <<Import name>>\n
    <<short Explanation>>
    \n
    (for classes and functions)\n
    ### <<Class, Function name>>\n
     <<Code snippet>> \n
    <<Explanation>>
    \n
    (for anything else)
    <<Code snippet (body text)>>\n
    <<Explanation>>
    
    \n\n Context - {context} \n\n Next chunk of code- {chunk}"""
    summaries = []
    for chunk in chunks:
        prompt = PromptTemplate.from_template(prompt_template)
        llm_chain = prompt | llm
        response = llm_chain.invoke({'chunk' : chunk, 'context' : chunks[0] })
        summaries.append(response)
    summ = ""
    for line in summaries:
        summ +=str(line.content) + "\n\n"
    return summ
