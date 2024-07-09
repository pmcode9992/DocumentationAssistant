from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI 
from dotenv import load_dotenv
import os
from utils.textSplit import getChunks

load_dotenv()
API_KEY = os.getenv("SingleSession_APIKEY")

def sumChunks(shortSummary, code):
   
    splits = getChunks(code)
    chunks = [shortSummary]
    for i in splits:
        chunks.append(i.page_content)
    

    llm = OpenAI(api_key=API_KEY) 

    prompt_template = " {context} Explain this chunk of code (return the same text if it's not a codefile) {chunk}\n\nGuidelines \n- Output should be Markdown formatted\n- In order of their occurence in the codefile \n- Include important code snippets if needed \n- Explain what the code does\n Order of contents is Function(/import/class etc) name (third-level heading) followed by explanation of that function"
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
