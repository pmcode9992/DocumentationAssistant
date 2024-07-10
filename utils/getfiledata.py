def getFileData(pth):
    code_snippet = ""
    with open(pth, "r") as file:
        try:
            code_snippet = file.read()
        except:
            return "Unreadable file"
    return code_snippet

