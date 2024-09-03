from utils.getfiledata import getFileData
import os

def getProjectStructure(pth, unwanted_files):   
    l=[]
    
    if os.path.isdir(pth):
        l = os.listdir(pth)
        l = list(filter(lambda x : x not in unwanted_files, l))
        for i in range(0, len(l)):
            if(os.path.isdir(pth + "/" + l[i])):
                l[i] = getProjectStructure((pth + "/" + l[i]), unwanted_files)
            else:
                l[i] = {(l[i]) : getFileData(str(pth + "/" + l[i]))}
    return {"📁 :"+os.path.basename(pth) : l}

def getFolderStructure(pth, unwanted_files):   
    l=[]
    if os.path.isdir(pth):
        l = os.listdir(pth)
        l = list(filter(lambda x : x not in unwanted_files, l))
        for i in range(0, len(l)):
            if(os.path.isdir(pth + "/" + l[i])):
                l[i] = getFolderStructure((pth + "/" + l[i]), unwanted_files)
            else:
                l[i] = {l[i] : None}
    return {"📁 :"+os.path.basename(pth) : l}
