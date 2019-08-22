import os
from pathlib import Path
import shutil
import glob


# Moving a file from one dir to another
def move_file(srcFile, destDir):
        if Path(srcFile).is_file():
            shutil.move(str(srcFile), str(destDir))


# Move all files of one extension from src to dest
def move_files(src, dest, ext=""):
        filenames = os.listdir(str(src))
        for filename in filenames:
                filePath = Path(src) / (filename)
                destPath = Path(dest) / (filePath.name)
                # if fnmatch.fnmatch(file, '*.csv'):
                print (filePath)
                print (destPath)
                if filename.endswith(ext):
                        shutil.move(str(filePath), str(destPath))
    
    
# Moving dir from source to destination
def move_dir(src, dest):
        if Path(src).is_dir():
            shutil.move(str(src), str(dest))


# Moving multiple files from one folder to the other based on text characters in file name
def move_files_based_on_text(src, dest, string, isSensitive):
        filenames = os.listdir(str(src))
        for filename in filenames:
                filePath = Path(src) / (filename)
                destPath = Path(dest) / (filePath.name)
                if isSensitive is True:
                        if string in filename:
                                shutil.move(str(filePath), str(destPath))
                else:
                        if string.upper() in filename.upper():
                                shutil.move(str(filePath), str(destPath))


# Getting list of file paths in a directory based on text characters in file name
def get_file_paths_by_substr(dirPath, string, isSensitive):
        filesPath = [os.path.abspath(x) for x in os.listdir(dirPath)]
        print(filesPath)

        returnList = []
        for path in filesPath:
                if isSensitive is True:
                        if string in path:
                                returnList.append(path)
                else:
                        if string.upper() in path.upper():
                                returnList.append(path)
        return returnList

# mylist = get_file_paths_by_substr(filesPath, "error", False)
# print("Mylist-", mylist)


# This function accepts a list of strings and a glob pattern and 
#       returns a new list with the strings from the list that match that glob pattern

def filter_by_glob(collection, pattern):
        parts = pattern.split("*")
        begining = parts[0]
        ending = parts[1]

        newList = []

        for item in collection:
                # item = str(item)
                strItem = str(item)
                if strItem.startswith(begining) and strItem.endswith(ending):
                        newList.append(strItem)
        return newList