import os
from pathlib import Path
import shutil


def move_file(srcFile, destDir):
    """Moves a file from one dir to another"""
    if Path(srcFile).is_file():
        shutil.move(str(srcFile), str(destDir))


def move_files(src, dest, ext=""):
    """Moves all files of one extension from src to dest"""
    filenames = os.listdir(str(src))
    for filename in filenames:
        filePath = Path(src) / (filename)
        destPath = Path(dest) / (filePath.name)
        # if fnmatch.fnmatch(file, '*.csv'):
        print(filePath)
        print(destPath)
        if filename.endswith(ext):
            shutil.move(str(filePath), str(destPath))


def move_dir(src, dest):
    """Moves dir from source to destination"""
    if Path(src).is_dir():
        shutil.move(str(src), str(dest))


def move_files_based_on_text(src, dest, string, isSensitive):
    """
    Moves multiple files from one folder to the other based on text characters in file name
    """
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


def get_file_paths_by_substr(dirPath, string, isSensitive):
    """
    Gets list of file paths in a directory based on text characters in file name
    """
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


def zipdir(source_dir, zipname=None):
    """
    Creates a zip archive which contains the directory specified in dirPath.

    Args:
        source_dir: Path or str representing absolute directory path
        zipname (str, optional): Name of the generated archive. If not
            provided, the name defaults to the directory's name.

    Returns:
        Path for the zip archive created in the source_dir's parent dir

    Raises:
        ValueError if source is an invalid directory
    """
    source = Path(source_dir)

    if not source.is_dir():
        raise ValueError(f"{source} is not a valid directory")

    dest = source.parent

    # chdir to create the zip in the parent dir
    os.chdir(dest)

    if zipname is None:
        zipname = source.name
    print("zipname: " + zipname)

    shutil.make_archive(zipname, format="zip", root_dir=source)

    return dest.joinpath(zipname + ".zip")


def zipfiles(file_paths, dest_dir, zipname):
    """
    Creates a zip archive from list of file paths in destination.

    Args:
        file_paths: List of Path objects or strings
        dest_dir: Path to directory where zip will be generated
        zipname: Name of the zip archive

    Returns:
        Path for the zip archive created

    Raises:
        ValueError if dest dir is invalid
    """
    # convert to Path objects
    dest = Path(dest_dir)
    files = [Path(f) for f in file_paths]

    if not dest.is_dir():
        raise ValueError(f"{dest} is not a valid directory")

    os.chdir(dest)

    # copy all files in the list to a temp dir in dest
    temp_dir = dest / "temp"
    if temp_dir.is_dir():
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)

    for f in files:
        shutil.copyfile(f, temp_dir / f.name)

    shutil.make_archive(zipname, format="zip", root_dir=temp_dir)

    shutil.rmtree(temp_dir)

    return dest.joinpath(zipname + ".zip")
