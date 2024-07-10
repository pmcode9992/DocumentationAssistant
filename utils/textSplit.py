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
    
    with open("splits.md", "w") as f:
        f.write(str(len(splits)) + "\n")
        for line in splits:
            f.write(str(line) + "\n\n")
        f.close()
    return splits
