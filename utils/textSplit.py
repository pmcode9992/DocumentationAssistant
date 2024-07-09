from langchain_text_splitters import (RecursiveCharacterTextSplitter, Language)

def getChunks(code):
    splits = []
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language= Language.PYTHON,
        chunk_size=3000,
        chunk_overlap=750
    )
    splits = text_splitter.create_documents([code])
    
    with open("splits.md", "w") as f:
        f.write(str(len(splits)) + "\n")
        for line in splits:
            f.write(str(line) + "\n\n")
        f.close()
    return splits

# text = []
# with open("decisiontree.py") as f:
#     code = f.read()
#     text = getChunks(code)
#     print(len(text))
#     f.close()


    