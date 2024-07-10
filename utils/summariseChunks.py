from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI 
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
    

    llm = OpenAI(api_key=API_KEY) 

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
    
    \n\n Context - {context[0]} \n\n Next chunk of code- {chunk}"""
    summaries = []
    for chunk in chunks:
        cntxt = str(summaries)
        prompt = prompt_template.format(context=cntxt, chunk=chunk)
        response = llm.generate(prompts=[prompt])
        summaries.append(response.generations[0][0].text)

    with open("summaries.md", "w") as f:
        for line in summaries:
            f.write(str(line) + "\n\n")
        f.close()
    
    summ = ""
    with open("summaries.md") as f:
        summ = f.read()
        f.close()
    return summ
