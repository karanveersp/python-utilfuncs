import os
import shutil
import datetime
import base64
import chardet
import codecs
from pathlib import Path
from tempfile import TemporaryDirectory, tempdir
from typing import List, Sequence, Union
from zipfile import ZipFile, ZIP_DEFLATED

from utilfuncs.common import *


def create_dir_if_not_exists(dirpath: PathLike) -> None:
    """
    Creates a directory and all intermediate directories if they don't exist

    Args:
        dirpath: Path to dir
    """
    if not dirpath.is_dir():
        os.makedirs(dirpath, exist_ok=True)


def get_base64_encoded_contents(filepath: PathLike) -> str:
    """
    Returns a b64 encoded string representing file contents

    Args:
        filepath: Path to file
    
    Returns:
        B64 encoded string
    """
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_ext(filepath: PathLike) -> str:
    """
    Returns the extension of the file with prepended period (.)
    Example:
        Fetching extension::
        
            >>> get_ext("file.txt")
            ".txt"

    Args:
        filepath: Path of file
    
    Returns:
        Period prefixed extension for the given file
    """
    return "." + filepath.name.split(".")[1]


def rename_file(filepath: PathLike, new_name: str) -> PathLike:
    """
    Renames the given file with new name and returns path to renamed file.
    

    Args:
        filepath: Path to existing file
        new_name: New name to apply
    
    Returns:
        Path to renamed file
    """
    new_name_with_ext = new_name + get_ext(filepath)
    renamed_file_path = Path(filepath).parent / new_name_with_ext
    os.replace(filepath, renamed_file_path)
    return renamed_file_path


def move_file(src_file: PathLike, dest_dir: PathLike) -> PathLike:
    """
    Moves file to dest dir and returns file path in destination.

    Args:
        src_file: Path to src
        dest_dir: Path to dir

    Returns:
        Path of file in destination
    """

    destpath = Path(dest_dir) / src_file.name
    if destpath.is_file():
        os.remove(destpath)
    shutil.move(str(src_file), str(destpath))
    return destpath


def move_files(src_dir: PathLike, dest_dir: PathLike, ext="") -> None:
    """
    Moves all files of one extension from src to dest

    Args:
        src_dir: Source directory containing files to move
        dest_dir: Destination directory
        ext (str, optional): Target files to move by extension. Defaults to "".
    """
    filenames = os.listdir(src_dir)
    for name in filenames:
        filepath = Path(src_dir) / name
        if name.endswith(ext) and filepath.is_file():
            move_file(filepath, dest_dir)


def move_dir(src: PathLike, dest: PathLike) -> PathLike:
    """
    Moves dir from source to destination and returns new dir path.

    Args:
        src: Path to src
        dest: Path to new parent dir

    Returns:
        Path to directory under dest
    """
    shutil.move(str(src), str(dest))
    return Path(dest) / src.name


def move_files_matching_regex(src_dir: PathLike, dest_dir: PathLike, pattern: str) -> None:
    """
    Moves files matching regex to destination, non recursively.

    Args:
        src_dir: Path to src dir
        dest_dir: Path to dest dir
        pattern: Glob pattern
    """
    files = Path(src_dir).glob(pattern)
    for path in files:
        # skip dirs
        if not path.is_file():
            continue
            
        move_file(path, dest_dir)


def zipdir(dirpath: PathLike, zip_path: PathLike = None, delete_dir_afterwards=False, top_level_dir=True) -> Path:
    """
    Creates a zip archive which contains the directory specified in dirPath.

    Args:
        dirpath: Path to directory
        zip_path (PathLike, optional): Path to final zip file including name.
            If not provided, the zip file is written in dirpath's parent with the
            dirpath name and .zip extension.
        delete_dir_afterwards (bool, optional): Whether to delete the orignal dir
            after compression. Defaults to False.
        top_level_dir (bool, optional): Whether to have dirpath folder
            inside the zip or to have dirpath files directly inside the zip. Defaults to True.

    Returns:
        Path of compressed zip file
    """
    
    if not Path(dirpath).is_dir():
        raise InvalidDirectoryPath(f"{dirpath} is not a valid directory")

    resolved_path = Path(dirpath).expanduser().resolve(strict=True)

    final_zip_path = zip_path if zip_path is not None else (resolved_path.parent / (resolved_path.name + ".zip"))
    with ZipFile(final_zip_path, "w", ZIP_DEFLATED) as zf:
        for path in resolved_path.rglob("*"):
            rel_to_top_level = path.relative_to(resolved_path.parent) if top_level_dir else path.relative_to(resolved_path)
            zf.write(path, rel_to_top_level)
    
    if delete_dir_afterwards:
        shutil.rmtree(str(dirpath))

    return final_zip_path


def zipfiles(zip_path: PathLike, files_or_directories: Sequence[PathLike]) -> None:
    """
    Creates a zip archive from list of file or directory paths in destination.

    Args:
        zip_path: Path of zip file with proper name and extension
        file_paths: List of Paths
    """
    with TemporaryDirectory() as temp:

        for f in files_or_directories:
            if Path(f).is_dir():
                shutil.copytree(f, Path(temp) / f.name)
            else:
                shutil.copyfile(f, Path(temp) / f.name)

        zipdir(temp, zip_path, top_level_dir=False)


def get_contents_as_utf8(filepath: PathLike) -> str:
    """
    Returns a string representing contents of the file converted to
    utf-8.

    Args:
        filepath: Path to file

    Returns:
        File content as utf-8 string
    """
    with open(filepath, "rb") as f:
        content_bytes = f.read()
        detected = chardet.detect(content_bytes)
        file_encoding = detected["encoding"]
        # print(f"{filepath}: detected as {file_encoding}."
        if "utf-8" in file_encoding.lower():
            return filepath
        elif file_encoding is None:
            content_text = codecs.decode(content_bytes)
        else:
            content_text = codecs.decode(content_bytes, file_encoding, errors="replace")

    return codecs.encode(content_text, "utf-8", errors="replace")


def all_files_under(dirpath: PathLike, extension="") -> List[Path]:
    """
    Iterates through all files that are under the given dir with the given extension ex '.log'

    Args:
        path: The directory to scan
        extension (str, optional): The extensions to consider if provided (with period)
    Returns:
        List of Path objects or empty list if no files in directory
    """
    results = []

    try:
        currpath, _, filenames = next(os.walk(dirpath))  # only traverse one level
    except StopIteration:
        # means no files in log folder
        return results

    for name in filenames:
        if extension in name:  # empty string extension will match all files
            results.append(Path(currpath) / name)

    return results


def delete_old_files(dirpath: PathLike, days: int, extension="") -> List[Path]:
    """
    Deletes files older than a certain number of days in a given folder and returns a list of
    files that were deleted.
    Non recursive.

    Args:
        dirpath: Path for directory
        days: Age of files in days
        extension (str, optional): File extension including period prefix
    
    Returns:
        List of files that were deleted
    """
    num_days = -1 * days
    days_ago = datetime.datetime.now() + datetime.timedelta(num_days)

    filepaths = all_files_under(dirpath, extension)

    deleted = []

    for f in filepaths:
        last_m_time = datetime.datetime.fromtimestamp(f.stat().st_mtime)
        if last_m_time < days_ago:
            os.remove(f)
            deleted.append(f)
    
    return deleted
