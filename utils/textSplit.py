from langchain_text_splitters import (RecursiveCharacterTextSplitter, Language)

def getChunks(code, lang):
    l = "CPP"
    if lang == "py":
        lang = "python"
    for e in Language:
        if e.value == lang:
            l = e.name
            
            
    splits = []
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language= getattr(Language, l ),
        chunk_size=1500,
        chunk_overlap=300
    )
    splits = text_splitter.create_documents([code])
    return splits
