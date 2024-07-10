import os

def formatSummary(filestr, summary, indent = 0):
    output = ""
    if isinstance(filestr, dict):
        for item, value in filestr.items():
            if (value is None) and (not summary):
                output += ("     " * indent+ f"{item}\n")
            elif isinstance(value, str) and summary:
                output += f"#{item}\n\n{value}\n"
            else:
                output += formatSummary(value, summary, indent + 1)
    else:
        for i in filestr:
            output += formatSummary(i, summary, indent)
    return output
        

def genMarkdown(projName, projSummary, folderstr, longSummary):
    file_contents = ""
    file_path = ""
    try:
        current_path = os.getcwd()
        file_path = os.path.join(current_path, f"{projName}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"## {projName}\n\n")
            f.write(projSummary)
            f.write("\n\n")
            formatted_folderstr = formatSummary(folderstr, False)
            f.write(formatted_folderstr)
            f.write("\n\n")
            formatted_longSummary = formatSummary(longSummary, True)
            f.write(formatted_longSummary)
            f.close()
    except:
        print("DIDNT MAKE FILE")
    with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
    return [file_contents, file_path]
    
