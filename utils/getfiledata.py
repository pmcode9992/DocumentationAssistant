def getFileData(pth):
    summary = ""
    code_snippet = ""
    with open(pth, "r") as file:
        try:
            code_snippet = file.read()
            try: 
                summary = code_snippet
            except:
                return "Error summarising"
        except:
            return "Unreadable file"
    return summary

